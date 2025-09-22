import datetime
import os
import time
from pprint import pprint

import queue, threading
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

import whisper


q = queue.Queue()
recording = False


def complicated_record():
    with sf.SoundFile(
        f'records/{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.wav',
        mode='w',
        samplerate=16000,
        subtype='PCM_16',
        channels=1,
    ) as file:
        with sd.InputStream(
            samplerate=16000, dtype='int16', channels=1, callback=complicated_save
        ):
            while recording:
                file.write(q.get())


def complicated_save(indata, frames, time, status):
    q.put(indata.copy())


def pre_record():
    os.makedirs('records', exist_ok=True)

    devices = sd.query_devices(kind='input')
    if len(devices) == 0:
        return False
    return True


def record():
    global recording

    if not pre_record():
        print("사용 가능한 입력 장치가 없습니다.")
        return

    recording = True
    recorder = threading.Thread(target=complicated_record)
    recorder.start()
    print('Recording...')

    input('Press Enter to stop recording...\n')

    recording = False
    recorder.join()
    print('Recording stopped.')


def get_filelist():
    return [f for f in os.listdir('records') if f.endswith('.wav')]


def select_file():
    filelist = get_filelist()
    for i, f in enumerate(filelist):
        print(f'{i + 1}: {f}')
    selected = int(input('Select a file by number: '))
    return filelist[selected - 1]


def transcribe_with_timestamps(filename):
    real_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'records', filename
    )
    model = whisper.load_model('base')
    result = model.transcribe(real_path, word_timestamps=True)

    with open(f'{real_path[:real_path.rfind(".")]}.CSV', 'w') as f:
        f.write('start,end,text\n')
        for segment in result['segments']:
            print(f'{segment['start']:.2f}s - {segment['end']:.2f}s: {segment['text']}')
            f.write(
                f'{segment['start']:.2f},{segment['end']:.2f},{segment['text'].strip()}\n'
            )


if __name__ == '__main__':
    try:
        record()
        selected = select_file()
        transcribe_with_timestamps(selected)
    except Exception as e:
        print(e)
