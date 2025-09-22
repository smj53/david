import zipfile
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def unzip():
    local_zip = 'cctv.zip'
    zip_ref = zipfile.ZipFile(local_zip, 'r')
    zip_ref.extractall('cctv')
    zip_ref.close()

    print(f"Unzipped files to {os.path.abspath('cctv')}")


def show_images():
    img_dir = 'cctv'
    img_files = sorted([f for f in os.listdir(img_dir) if f.endswith('.jpg')])

    if not img_files:
        print("No images found!")
        return

    current_idx = 0

    fig, ax = plt.subplots(figsize=(12, 8))

    def show_current_image():
        ax.clear()
        img_path = os.path.join(img_dir, img_files[current_idx])
        img = mpimg.imread(img_path)
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(
            f'{img_files[current_idx]} ({current_idx + 1}/{len(img_files)})',
            fontsize=14,
            pad=20,
        )
        plt.tight_layout()
        fig.canvas.draw()

    def on_key(event):
        nonlocal current_idx

        if event.key in ['right', 'd']:
            current_idx = (current_idx + 1) % len(img_files)
            show_current_image()
        elif event.key in ['left', 'a']:
            current_idx = (current_idx - 1) % len(img_files)
            show_current_image()
        elif event.key == 'q' or event.key == 'escape':
            plt.close(fig)

    # 키보드 이벤트 연결
    fig.canvas.mpl_connect('key_press_event', on_key)

    # 첫 번째 이미지 표시
    show_current_image()

    plt.show()


def find_human():
    import cv2
    import numpy as np

    img_dir = 'cctv'
    img_files = sorted([f for f in os.listdir(img_dir) if f.endswith('.jpg')])

    # HOG 사람 검출기 초기화
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    for img_file in img_files:
        img_path = os.path.join(img_dir, img_file)
        image = cv2.imread(img_path)

        if image is None:
            print(f"Failed to load image {img_path}")
            continue

        # 이미지 크기 조정 (너무 큰 이미지는 처리 속도 저하)
        scale_percent = 60  # 이미지 크기를 60%로 줄임
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        # 사람 검출
        boxes, weights = hog.detectMultiScale(image, winStride=(8, 8))
        print(f"Detected {len(boxes)} humans in {img_file}")
        # 검출된 사람 주위에 사각형 그리기
        for x, y, w, h in boxes:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 결과 이미지 표시
        cv2.imshow('Human Detection', image)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q') or key == 27:  # 'q' 또는 'ESC' 키를 누르면 종료
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    unzip()
    show_images()

    find_human()
