import os
import zipfile
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import cv2
from ultralytics import YOLO
import torch


def unzip():
    local_zip = 'cctv.zip'
    if not os.path.exists(local_zip):
        print('zip 파일이 없습니다:', local_zip)
        return
    with zipfile.ZipFile(local_zip, 'r') as zf:
        zf.extractall('cctv')
    print(f"Unzipped files to {os.path.abspath('cctv')}")


def show_images():
    """(Optional) 이미지 미리보기. 좌우 화살표로 이동, q 종료."""
    # matplotlib.use('TkAgg')  # Ensure interactive backend (optional depending on env)

    img_dir = 'cctv'
    if not os.path.isdir(img_dir):
        print('디렉토리 없음:', img_dir)
        return
    img_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith('.jpg')])
    if not img_files:
        print('이미지 없음')
        return

    idx = 0
    fig, ax = plt.subplots(figsize=(10, 6))
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


def find_human_yolo(conf_threshold: float = 0.25, iou_threshold: float = 0.45):
    """YOLOv8 기반 사람(person class=0) 탐지 및 시각화."""
    img_dir = 'cctv'
    if not os.path.isdir(img_dir):
        print('디렉토리 없음:', img_dir)
        return
    img_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith('.jpg')])
    if not img_files:
        print('이미지 없음')
        return

    try:
        model = YOLO('yolov8n.pt')  # 첫 실행 시 다운로드
    except Exception as e:
        print('YOLO 모델 로드 실패:', e)
        return

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if device == 'cpu':
        print('[알림] GPU 미사용(CPU). 처음은 느릴 수 있습니다.')

    for img_file in img_files:
        path = os.path.join(img_dir, img_file)
        image = cv2.imread(path)
        if image is None:
            print('로드 실패:', path)
            continue

        try:
            results = model.predict(
                source=image,
                classes=[0],  # person only
                conf=conf_threshold,
                iou=iou_threshold,
                verbose=False,
                device=device,
            )
        except Exception as e:
            print(f'[{img_file}] 추론 실패:', e)
            continue

        if not results:
            print(f'[{img_file}] 결과 없음')
            continue

        r = results[0]
        boxes = r.boxes
        vis = image.copy()
        count = 0
        if boxes is not None and len(boxes) > 0:
            for b in boxes:
                xyxy = b.xyxy[0].int()
                x1, y1, x2, y2 = xyxy.tolist()
                conf = float(b.conf.item()) if b.conf is not None else 0.0
                if conf < conf_threshold:
                    continue
                count += 1
                cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 200, 0), 2)
                cv2.putText(
                    vis,
                    f'person {conf:.2f}',
                    (x1, max(12, y1 - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 200, 0),
                    1,
                    cv2.LINE_AA,
                )
        print(f'[{img_file}] 사람 검출 {count}개')
        cv2.imshow('YOLO Person Detection', vis)
        key = cv2.waitKey(0) & 0xFF
        if key in (ord('q'), 27):  # q or ESC
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    unzip()
    show_images()
    find_human_yolo(conf_threshold=0.2)
