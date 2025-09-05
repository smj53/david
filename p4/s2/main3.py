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
    return rfn.join_by('parts', merged, a3, jointype='inner')


def average(arr):
    avg_values = (arr['strength1'] + arr['strength2'] + arr['strength']) / 3
    return rfn.append_fields(arr, 'average', avg_values)


def filter_average_lt(arr, limit=50):
    return arr[arr['average'] < limit]


def array_to_csv(arr, filename='parts_to_work_on.csv'):
    np.savetxt(
        filename,
        arr,
        delimiter=',',
        fmt=['%s', '%.3f', '%.3f', '%.3f', '%.3f'],
        header='parts,strength1,strength2,strength3,average',
        comments='',
    )


def main():
    arr1 = file_to_nparray('mars_base_main_parts-001.csv')
    arr2 = file_to_nparray('mars_base_main_parts-002.csv')
    arr3 = file_to_nparray('mars_base_main_parts-003.csv')

    parts = merge_array(arr1, arr2, arr3)
    average_parts = average(parts)
    filtered = filter_average_lt(average_parts, 50)
    array_to_csv(filtered)


if __name__ == '__main__':
    main()
