import speech_recognition as sr
from os import path
import datetime
import time
from pprint import pprint

import whisper


def record(r):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something!')
        audio = r.listen(source)
    with open(f'{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.wav', 'wb') as f:
        f.write(audio.get_wav_data())


def stt(r):
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), 'output.wav')
    audio = sr.AudioData.from_file(AUDIO_FILE)
    try:
        pprint(r.recognize_google(audio, language='ko-KR', show_all=True))
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print(
            'Could not request results from Google Speech Recognition service; {0}'.format(
                e
            )
        )


def transcribe_with_timestamps(audio_file):
    model = whisper.load_model('base')
    result = model.transcribe(audio_file, word_timestamps=True)

    for segment in result['segments']:
        print(f'{segment['start']:.2f}s - {segment['end']:.2f}s: {segment['text']}')


try:
    r = sr.Recognizer()

    record(r)
    time.sleep(2)
    # stt(r)
    transcribe_with_timestamps(
        path.join(path.dirname(path.realpath(__file__)), 'output.wav')
    )
except Exception as e:
    print(e)
