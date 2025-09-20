import time
import zipfile
import itertools
import multiprocessing

ZIP_PATH = 'emergency_storage_key.zip'


def unlock_zip():
    start = time.time()

    attempts = 0
    event = multiprocessing.Event()
    queue = multiprocessing.Queue()
    parts = [b'abcdef', b'ghijkl', b'mnopqr', b'stuvwx', b'yz0123', b'456789']
    processes = [
        multiprocessing.Process(
            target=try_open, args=(ZIP_PATH, part, queue, event), daemon=True
        )
        for part in parts
    ]
    for p in processes:
        p.start()

    while not event.is_set():
        time.sleep(5)

    end = time.time()

    for p in processes:
        p.join()

    while not queue.empty():
        attempts += queue.get()

    print(f"시도 횟수(대략): {attempts}")
    print('시작 시간:', time.strftime('%Y.%m.%d - %H:%M:%S'))
    print(f'진행 시간: {end - start} seconds')


def check_password(zip, password):
    try:
        name = zip.namelist()[0]
        with zip.open(name, 'r', pwd=password) as f:
            f.read(1)  # 최소 읽기
        print('opened!')
        return True
    except Exception:
        return False


def try_open(path, part, queue, event):
    alpha = b'abcdefghijklmnopqrstuvwxyz0123456789'
    attempts = 0
    start = time.time()
    last_report = start
    total = len(alpha) ** 5 * len(part)
    name = multiprocessing.current_process().name
    with zipfile.ZipFile(path, 'r') as zf:
        for ch in part:
            for perm in itertools.product(alpha, repeat=5):
                attempts += 1
                password = bytes((ch, *perm))
                if check_password(zf, password):
                    event.set()
                    print('found: ', password)
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        zip_ref.extractall(pwd=password)
                    queue.put(attempts)
                    return
                now = time.time()
                if now - last_report >= 5:
                    if event.is_set():
                        queue.put(attempts)
                        return
                    print(f'[{name}] Attempts: {attempts / total * 100:.3f}%')
                    last_report = now


def main():
    try:
        unlock_zip()
    except Exception as e:
        print('Error occured: ', e)
    except KeyboardInterrupt:
        print('terminated')


if __name__ == '__main__':
    main()
