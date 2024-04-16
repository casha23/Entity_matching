import csv
import multiprocessing
import os
import sys

from lines import proccess_row


def main(csv_path):
    print("The process is started. The result will be saved in the 'result.txt'")
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'results.txt')
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

        with open(csv_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
            pool.map(proccess_row, csv_reader)
            pool.close()
            pool.join()
    except FileNotFoundError:
        print(f"File '{csv_path}' not found")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('For start: python start.py /path/to/file.csv')
    else:
        csv_path = sys.argv[1]
        main(csv_path)
