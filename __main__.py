#!/usr/bin/python
import sys
from combiner import Menu

if __name__ == "__main__":
    menu = Menu(
        'csv_data_1.csv',
        'csv_data_2.csv',
        'json_data.json',
        'xml_data.xml')
    menu.run()