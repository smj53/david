import csv


def print_list(lst):
    for e in lst:
        print(e)


def csv_to_list(filename):
    with open(filename, 'r') as f:
        content = f.read()
        print(content)
    with open(filename, 'r') as f:
        read = csv.reader(f)
        next(read)
        return list(read)


def sort_flammability_desc(lst):
    return sorted(lst, key=lambda e: float(e[4]), reverse=True)


def filter_flammability_7(lst):
    filtered = list(filter(lambda e: float(e[4]) >= 0.7, lst))
    print_list(filtered)
    return filtered


def list_to_csv(lst):
    with open('Mars_Base_Inventory_danger.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(
            [
                'Substance',
                'Weight (g/cm³)',
                'Specific Gravity',
                'Strength',
                'Flammability',
            ]
        )
        write.writerows(lst)


if __name__ == '__main__':
    try:
        lst = csv_to_list('Mars_Base_Inventory_List.csv')
        sorted = sort_flammability_desc(lst)
        filtered = filter_flammability_7(sorted)
        list_to_csv(filtered)
    except FileNotFoundError:
        print('파일이 존재하지 않습니다.')
    except IOError as e:
        print('입출력 에러: ', e)
    except Exception as e:
        print('에러:', e)
