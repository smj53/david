import random
import time
import psutil
import threading
import platform
import multiprocessing
import json


# 문제 1
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0,
        }
        self.limits = {
            'mars_base_internal_temperature': (18, 30),
            'mars_base_external_temperature': (0, 21),
            'mars_base_internal_humidity': (50, 60),
            'mars_base_external_illuminance': (500, 715),
            'mars_base_internal_co2': (0.02, 0.1),
            'mars_base_internal_oxygen': (4, 7),
        }
        self.names = [
            'mars_base_internal_temperature',
            'mars_base_external_temperature',
            'mars_base_internal_humidity',
            'mars_base_external_illuminance',
            'mars_base_internal_co2',
            'mars_base_internal_oxygen',
        ]
        self.set_env()

    def set_env(self):
        for name in self.names:
            min = self.limits[name][0]
            max = self.limits[name][1]
            self.env_values[name] = random.uniform(min, max)

    def get_env(self):
        self.set_env()
        return self.env_values


# 문제 2
class MissionComputer:
    def __init__(self, name='missionComputer'):
        self.env_values = {}
        self.ds = DummySensor()
        self.cpu_print_seconds = 20
        self.sensor_seconds = 5
        self.name = name

    def get_sensor_data1(self):
        while True:
            self.env_values = self.ds.get_env()
            self.print_json('env_values', self.env_values)
            time.sleep(self.sensor_seconds)

    # 문제 3
    def get_mission_computer_info1(self):
        # 운영체계, 운영체계 버전, CPU의 타입, CPU의 코어 수, 메모리의 크기
        infos = {
            'os': platform.system(),
            'os version': platform.release(),
            'cpu type': platform.machine(),
            'cpu core count': psutil.cpu_count(),
            'memory size': psutil.virtual_memory().total,
        }
        self.print_json('computer info', infos)

    def get_mission_computer_load1(self):
        # CPU 실시간 사용량, 메모리 실시간 사용량
        memory_dict = dict(psutil.virtual_memory()._asdict())
        infos = {
            'cpu runtime usage': psutil.cpu_percent(),
            'memory runtime usage': memory_dict['percent'],
        }
        self.print_json('cpu, memory info', infos)

    # 문제 4
    def get_sensor_data(self, lock):
        while True:
            self.env_values = self.ds.get_env()
            self.print_json_lock('env_values', self.env_values, lock)
            time.sleep(self.sensor_seconds)

    def get_mission_computer_info(self, lock):
        while True:
            infos = {
                'os': platform.system(),
                'os version': platform.release(),
                'cpu type': platform.machine(),
                'cpu core count': psutil.cpu_count(),
                'memory size': psutil.virtual_memory().total,
            }
            self.print_json_lock('computer info', infos, lock)
            time.sleep(self.cpu_print_seconds)

    def get_mission_computer_load(self, lock):
        # CPU 실시간 사용량, 메모리 실시간 사용량
        while True:
            memory_dict = dict(psutil.virtual_memory()._asdict())
            infos = {
                'cpu runtime usage': psutil.cpu_percent(),
                'memory runtime usage': memory_dict['percent'],
            }
            self.print_json_lock('cpu, memory info', infos, lock)
            time.sleep(self.cpu_print_seconds)

    def print_json(self, title, dic):
        print(f'[{self.name}: {title}]')
        print(json.dumps(dic, indent=2))
        print()

    def print_json_lock(self, title, dic, lock):
        with lock:
            self.print_json(title, dic)


# 문제 1
def prob1():
    print('문제 1================================')
    ds = DummySensor()
    ds.set_env()
    print(ds.get_env())


# 문제 2
def prob2():
    try:
        print('문제 2================================')
        RunComputer = MissionComputer('RunComputer')
        RunComputer.get_sensor_data1()
    except KeyboardInterrupt:
        print('System stoped….')


# 문제 3
def prob3():
    print('문제 3================================')
    runComputer = MissionComputer('runComputer')
    runComputer.get_mission_computer_info1()
    runComputer.get_mission_computer_load1()


# 문제 4
def multithreads():
    lock = threading.Lock()
    runComputer = MissionComputer('runComputer')
    threads = [
        threading.Thread(target=runComputer.get_sensor_data, daemon=True, args=(lock,)),
        threading.Thread(
            target=runComputer.get_mission_computer_info, daemon=True, args=(lock,)
        ),
        threading.Thread(
            target=runComputer.get_mission_computer_load, daemon=True, args=(lock,)
        ),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def multiprocesses():
    lock = multiprocessing.Lock()
    runComputer1 = MissionComputer('runComputer1')
    runComputer2 = MissionComputer('runComputer2')
    runComputer3 = MissionComputer('runComputer3')

    processes = [
        multiprocessing.Process(
            target=runComputer1.get_mission_computer_info, args=(lock,)
        ),
        multiprocessing.Process(
            target=runComputer2.get_mission_computer_load, args=(lock,)
        ),
        multiprocessing.Process(target=runComputer3.get_sensor_data, args=(lock,)),
    ]

    try:
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    except KeyboardInterrupt as e:
        for p in processes:
            if p.is_alive():
                p.terminate()
            p.join()
        raise e


def prob4():
    print('문제 4================================')
    try:
        option = input('multithreading 1, multiprocessing 2: ')
        match option:
            case '1':
                # thread
                multithreads()
            case '2':
                # process
                multiprocesses()
            case _:
                pass
    except KeyboardInterrupt:
        print('System stoped….')


if __name__ == '__main__':
    option = input('select probrom #: ')
    match option:
        case '1':
            prob1()
        case '2':
            prob2()
        case '3':
            prob3()
        case '4':
            prob4()
        case _:
            pass
