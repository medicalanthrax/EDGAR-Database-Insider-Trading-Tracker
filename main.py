"""Collect all the various methods into one"""

from collect_dirs import collect_dirs
from get_link import get_link
from read_data import read_data

def main():
    """Main"""
    for i in collect_dirs():
        print(
            read_data(
                get_link(i)
            )
        )
main()
