import csv
from io import StringIO, TextIOWrapper
from prettytable import PrettyTable, from_csv
from tabulate import tabulate

def crop_header(fp:TextIOWrapper )-> TextIOWrapper:
    """
    skip line of the file until the line is blank then reconstruct IO wrapper 
    with the reste of the line (should be the csv table)
    """
    table_start = 0
    for line_number, line in enumerate(fp):
        if line in ['\n','\r\n']: 
            table_start = line_number
    table_start += 1
    print(f"table start at line {table_start+1}")

    fp.seek(0)
    for l in range(table_start):
        next(fp)
        
    return StringIO(fp.read())


def print_csv_file(file):
    with open(file) as fp:
        fp = crop_header(fp)
        mytable = from_csv(fp)
        print(mytable)