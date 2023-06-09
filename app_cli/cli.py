#! venv/bin/python
# provides the application’s command-line interface. The code in this file will
# play the view-controller role in the MVC-based architecture.

import argparse
import csv
from pathlib import Path
import sys
import logging
import pandas as pd

from prettytable import PrettyTable, from_csv
from tabulate import tabulate
import controler
from front_tools import crop_header, detect_table_start, plot_df, print_table
from db_model import DataBase

logger = logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class Budget_tracker():
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Budjet tracker CLI',
            usage='''budget_tracker <command> [<args>]

Available commands are:
   display_csv     Record changes to the repository
''')
        parser.add_argument('command', help='Subcommand to run')
        parser.add_argument('-v', '--verbose', action="store_true")
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        
        if args.verbose :
            logger.setLevel(logging.DEBUG)

        # init database
        self.db = DataBase()
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    def display_csv(self):
        parser = argparse.ArgumentParser(
            description='Display a expences store in a csv file')
        parser.add_argument(
            "csv_file",
            help="csv file that you whant to diplay"
        )
        args = parser.parse_args(sys.argv[2:])

        target_file = Path(args.csv_file)
        if not target_file.exists():
            print("The target file doesn't exist")
            raise SystemExit(1)
        if target_file.suffix != ".csv":
            print("The target file is not a csv")
            raise SystemExit(1)
        
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        df_depences, df_revenus = controler.read_csv_from_bank(args.csv_file)
        self.db.add_categories(df_depences)
        self.db.add_categories(df_revenus)
        print("\nREVENUE")
        plot_df(df_revenus)
        print("\nDEPENSES:")
        plot_df(df_depences)
        self.db.save_data()

    def update(self):
        parser = argparse.ArgumentParser(
            description='Update the budget tracker history with a csv file')
        parser.add_argument(
            "csv_file",
            # nargs="?",
            help="csv file that you whant to use"
        )
        args = parser.parse_args(sys.argv[2:])



if __name__ == "__main__":
    Budget_tracker()
