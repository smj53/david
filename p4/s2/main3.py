import numpy as np
from numpy.lib import recfunctions as rfn


def file_to_nparray(filename):
    data = np.genfromtxt(
        filename,
        delimiter=',',
        skip_header=1,
        dtype=[('parts', 'U50'), ('strength', 'f8')],
    )
    return data


def merge_array(a1, a2, a3):
    merged = rfn.join_by('parts', a1, a2, jointype='inner')
    print('merged: ', merged)
    return rfn.join_by('parts', merged, a3, jointype='inner')


def numpy_mean(arr):
    strength_arrays = [
        arr[field] for field in arr.dtype.names if field.startswith('strength')
    ]
    avg_values = np.mean(np.stack(strength_arrays), axis=0)
    return rfn.append_fields(arr, 'average', avg_values)


def average(arr):
    # 동적으로 strength 관련 필드들을 찾아서 평균 계산
    strength_fields = [name for name in arr.dtype.names if name.startswith('strength')]

    if len(strength_fields) != 3:
        raise ValueError(
            f"Expected 3 strength fields, but found {len(strength_fields)}: {strength_fields}"
        )

    avg_values = sum(arr[field] for field in strength_fields) / len(strength_fields)
    return rfn.append_fields(arr, 'average', avg_values)


def filter_average_lt(arr, limit=50):
    return arr[arr['average'] < limit]


def array_to_csv(arr, filename='parts_to_work_on.csv'):
    np.savetxt(
        filename,
        arr,
        delimiter=',',
        fmt=['%s', '%.3f', '%.3f', '%.3f', '%.3f'],
        header=','.join(arr.dtype.names),
        comments='',
    )


def main():
    try:
        arr1 = file_to_nparray('mars_base_main_parts-001.csv')
        arr2 = file_to_nparray('mars_base_main_parts-002.csv')
        arr3 = file_to_nparray('mars_base_main_parts-003.csv')

        parts = merge_array(arr1, arr2, arr3)
        average_parts = average(parts)
        # average_parts = numpy_mean(parts)
        filtered = filter_average_lt(average_parts, 50)
        array_to_csv(filtered)
    except FileNotFoundError:
        print('파일이 존재하지 않습니다.')
    except IOError as e:
        print('입출력 에러: ', e)
    except ValueError as e:
        print('값 에러:', e)
    except Exception as e:
        print('에러:', e)


if __name__ == '__main__':
    main()
