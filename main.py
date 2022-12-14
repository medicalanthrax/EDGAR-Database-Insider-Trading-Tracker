"""Collect all the various methods into one and display"""
#pylint: disable=E0401
import csv
import time

from collect_dirs import collect_dirs
from get_link import get_link
from read_data import read_data


def main():
    """Main"""
    start = time.perf_counter()
    file = open("data.csv", mode='r', encoding="utf-8",newline="")
    my_reader = csv.reader(file)
    old_entries = []
    for lines in my_reader:
        old_entries.append(lines)
    file.close()
    old_entries = old_entries[1:]
    new_entries = []
    for directory in collect_dirs():
        print(directory)
        new_entries.append(
            read_data(
                get_link(
                    directory
                )
            )
        )
    file = open("data.csv", mode='w', encoding="utf-8",newline="")
    my_writer = csv.writer(file, delimiter=",")
    my_writer.writerow(['Date', 'Company', 'Title', 'Stock Title',
                       'Code', 'No. Shares', 'Price Per Share'])
    for i in new_entries:
        my_writer.writerow(i)
    for i in old_entries:
        my_writer.writerow(i)
    file.close()
    end = time.perf_counter()
    print(end-start)
#Uncomment to get csv viewer    t.view("data.csv")
main()
