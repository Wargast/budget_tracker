import csv
from io import StringIO, TextIOWrapper
from InquirerPy import inquirer
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

def detect_table_start(file):
    """
    skip line of the file until the line is blank then reconstruct IO wrapper 
    with the reste of the line (should be the csv table)
    """
    table_start = 0
    with open(file) as fp:
        for line_number, line in enumerate(fp):
            if line in ['\n','\r\n']: 
                table_start = line_number
        print(f"table start at line {table_start+1}")
    return table_start

def print_table(table):
    print(tabulate(table, headers="firstrow", tablefmt='rounded_grid'))

def select_category(category_list, default_cat):
    cat = inquirer.fuzzy(
        message="Select actions:",
        choices=category_list,
        default=default_cat,
    ).execute()
    return cat
