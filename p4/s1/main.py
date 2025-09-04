import pprint
import json


def read_csv(filename):
    print('=파일 읽기=')

    with open(filename, 'r', encoding='utf8') as f:
        content = f.read()
    return content


def convert_csv_to_list(csv_data):
    print('=csv를 리스트로 전환=')

    rows = csv_data.split('\n')
    list = []
    for row in rows[1:]:
        if not row:
            continue
        list.append(row.split(','))
    return list


def sort_time_desc(list):
    print('=시간 역순(내림차순) 정렬=')

    return sorted(list, key=lambda e: e[0], reverse=True)


def convert_list_to_dict(list):
    print('=리스트 -> 사전=')

    return dict(zip(map(lambda e: e[0], list), map(lambda e: e[1:], list)))


def save_dict_to_json(dict):
    print('=사전 객체 json 저장=')

    with open('mission_computer_main.json', 'w', encoding='utf8') as f:
        json.dump(dict, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    try:
        csv_data = read_csv('mission_computer_main.log')
        list = convert_csv_to_list(csv_data)
        pprint.pprint(list)

        sorted_list = sort_time_desc(list)
        pprint.pprint(sorted_list)

        dict = convert_list_to_dict(sorted_list)
        pprint.pprint(dict)

        save_dict_to_json(dict)

    except FileNotFoundError:
        print('파일이 존재하지 않습니다.')
    except IOError as e:
        print('입출력 에러: ', e)
    except Exception as e:
        print(e)
