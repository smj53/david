import os
import zipfile
import numpy as np

import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def unzip():
    local_zip = 'cctv.zip'
    if not os.path.exists(local_zip):
        print('zip 파일이 없습니다:', local_zip)
        return
    with zipfile.ZipFile(local_zip, 'r') as zf:
        zf.extractall('cctv')
    print(f"Unzipped files to {os.path.abspath('cctv')}")


def show_images():
    img_dir = 'cctv'
    if not os.path.isdir(img_dir):
        print('디렉토리 없음:', img_dir)
        return
    img_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith('.jpg')])
    if not img_files:
        print('이미지 없음')
        return

    idx = 0
    fig, ax = plt.subplots(figsize=(30, 30))
    fig.canvas.manager.set_window_title('Image Preview')

    def render():
        ax.clear()
        path = os.path.join(img_dir, img_files[idx])
        ax.imshow(mpimg.imread(path))
        ax.set_title(f'{img_files[idx]} ({idx+1}/{len(img_files)})')
        ax.axis('off')
        fig.canvas.draw()

    def on_key(event):
        nonlocal idx
        if event.key in ('right', 'd'):
            idx = (idx + 1) % len(img_files)
            render()
        elif event.key in ('left', 'a'):
            idx = (idx - 1) % len(img_files)
            render()
        elif event.key in ('q', 'escape'):
            plt.close(fig)

    fig.canvas.mpl_connect('key_press_event', on_key)
    render()
    plt.show()

    plt.cla()
    plt.clf()
    plt.close()


def apply_nms(boxes, scores, score_threshold, nms_threshold):
    """Non-Maximum Suppression 적용"""
    indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold, nms_threshold)
    return indices


# -------------- Refactor helpers --------------
INPUT_SIZE = 640


def preprocess(image, size: int = INPUT_SIZE):
    blob = cv2.dnn.blobFromImage(
        image,
        1 / 255.0,
        (size, size),
        swapRB=True,
        crop=False,
    )
    return blob


def forward(net):
    out = net.forward()
    # out can be (1, N, 85) or (N, 85)
    if isinstance(out, (list, tuple)):
        out = out[0]
    if getattr(out, 'ndim', 2) == 3:
        out = out[0]
    return out  # shape: (N, 85)


def parse_yolov5(outputs, width: int, height: int, conf_threshold: float):
    boxes = []
    scores = []
    scale_x = width / INPUT_SIZE
    scale_y = height / INPUT_SIZE

    for det in outputs:
        obj_conf = float(det[4])
        if obj_conf < conf_threshold:
            continue
        cls_scores = det[5:]
        class_id = int(np.argmax(cls_scores))
        cls_conf = float(cls_scores[class_id])
        conf = obj_conf * cls_conf
        if class_id != 0 or conf < conf_threshold:
            continue

        cx, cy, w, h = det[:4]
        cx *= scale_x
        cy *= scale_y
        w *= scale_x
        h *= scale_y

        x1 = int(cx - w / 2)
        y1 = int(cy - h / 2)
        x1 = max(0, min(x1, width))
        y1 = max(0, min(y1, height))
        w = max(0, min(int(w), width - x1))
        h = max(0, min(int(h), height - y1))

        boxes.append([x1, y1, w, h])
        scores.append(conf)

    return boxes, scores


def draw_detections(image, boxes, indices, scores):
    vis = image.copy()
    kept = 0
    if indices is not None and len(indices) > 0:
        # normalize indices shape
        if hasattr(indices, 'ndim') and indices.ndim > 1:
            indices = indices.flatten()
        for i in indices:
            x1, y1, w, h = boxes[int(i)]
            x2, y2 = x1 + w, y1 + h
            conf = float(scores[int(i)])
            cv2.rectangle(
                vis,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3,
            )
            text = f'person {conf:.2f}'
            ts, _ = cv2.getTextSize(
                text,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2,
            )
            cv2.rectangle(
                vis,
                (x1, max(0, y1 - 25)),
                (x1 + ts[0], y1),
                (0, 255, 0),
                -1,
            )
            cv2.putText(
                vis,
                text,
                (x1, max(12, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )
            kept += 1
    return vis, kept


# -------------- Main pipeline --------------


def find_human_opencv(
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.45,
):
    """OpenCV DNN 기반 사람(person) 탐지 및 시각화."""
    img_dir = 'cctv'
    if not os.path.isdir(img_dir):
        print('디렉토리 없음:', img_dir)
        return

    img_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith('.jpg')])
    if not img_files:
        print('이미지 없음')
        return

    # ONNX 모델 파일 로드
    onnx_model = 'yolov5n.onnx'
    try:
        net = cv2.dnn.readNetFromONNX(onnx_model)
        print('OpenCV DNN 모델 로드 성공')
    except Exception as e:
        print('OpenCV DNN 모델 로드 실패:', e)
        return

    idx = 0
    fig, ax = plt.subplots(figsize=(30, 30))
    fig.canvas.manager.set_window_title('Human Detection')

    def render():
        ax.clear()
        img_file = img_files[idx]
        path = os.path.join(img_dir, img_file)
        image = cv2.imread(path)
        if image is None:
            print('로드 실패:', path)
            return

        h_img, w_img = image.shape[:2]

        blob = preprocess(image)
        net.setInput(blob)
        try:
            outputs = forward(net)
            boxes, scores = parse_yolov5(outputs, w_img, h_img, conf_threshold)
        except Exception as e:
            print(f'[{img_file}] 추론 실패:', e)
            return

        if boxes:
            indices = apply_nms(boxes, scores, conf_threshold, iou_threshold)
            vis, count = draw_detections(image, boxes, indices, scores)
            print(f'[{img_file}] 사람 검출 {count}개')

            # out_path = f'result_{img_file}'
            # cv2.imwrite(out_path, vis)
            # print(f'결과 이미지 저장: {out_path}')
            img_rgb = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)
            ax.imshow(img_rgb)
        else:
            print(f'[{img_file}] 사람 검출 0개')
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            ax.imshow(img_rgb)

        ax.set_title(f'{img_files[idx]} ({idx+1}/{len(img_files)})')
        ax.axis('off')
        fig.canvas.draw()

    def on_key(event):
        nonlocal idx
        if event.key in ('enter'):
            idx += 1
            if idx == len(img_files):
                plt.close(fig)
            else:
                render()
        elif event.key in ('q', 'escape'):
            plt.close(fig)

    fig.canvas.mpl_connect('key_press_event', on_key)
    render()
    plt.show()
    print('검색 종료')


if __name__ == '__main__':
    unzip()
    show_images()
    find_human_opencv(conf_threshold=0.2)
