import csv
import re
from typing import Tuple
import pandas as pd
import dateparser

from front_tools import detect_table_start, select_category
import bdd_model

CATEGORY_LIST = [
    "🔨 Salaire",
    "💸 Alloc ",
    "🎁 Cadeau ",
    "🏦 Intérêts ",
    "🏡 Loyer ",
    "🥝 Courses ",
    "🍔 Restau ",
    "🚘 Transport ",
    "🛍 Shopping ",
    "📚 Loan ",
    "🍺 Drink ",
    "⚡️ Facture ",
    "💫 Personal ",
    "🧷 assurance ",
    "📞 Communication ",
    "💪 Sport ",
    "🧘‍♂️ Wellness ",
    "✈️ Vacances ",
    "🏡 Maison ",
    "👩‍⚕️ Santé ",
    "🎗 Cadeau ",
    "🍿 Loisirs ",
    "💵 Economies ",
    "autres",
]

def commentary_filter(str):
    ban_regex = [ "CARTE", "NUMERO", "ACHAT",
                    "CB", "CARTE", "687",
                    "[0-9]{2}\.[0-9]{2}\.[0-9]{2}",
                    "[0-9]{2}/[0-9]{2}/[0-9]{2}",
                    "EUR.*NO",
                    ":.*$",
                    "PRELEVEMENT DE ",
                    "([0-9]+[a-zA-Z]+|[a-zA-Z]+[0-9]+)([0-9]*[a-zA-Z]*)*",
                    "[0-9]{4}[0-9]*",]
    for r in ban_regex :
        str = re.sub(r, "", str)
    
    return str.strip()

def find_category(transaction, com: str):
    print(transaction)
    cat_guess = bdd_model.get_likely_cat()
    return select_category(CATEGORY_LIST, cat_guess)

def read_csv_from_bank(file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    with open(file) as fp:
        dialect = csv.Sniffer().sniff(fp.read(1024))
        df = pd.read_csv(
                file,
                header=detect_table_start(file),
                dialect=dialect,
                encoding_errors='ignore',
        )
        df.rename(
                columns={
                    df.columns[0]: "date",
                    df.columns[1]: "commentaire",
                    df.columns[2]: "montant",
                    },
                inplace=True
        )
        df["categorie"]="" # add empty column
        df["date"] = df["date"].astype('str')
        df = df.fillna('')
        df = df.reindex(
                columns=["date", "montant", "commentaire", "categorie"], 
        )
        df["montant"] = df["montant"].str.replace(",", ".") 

        df["commentaire"]= df["commentaire"].map(commentary_filter)
        for ind, com in enumerate(df["commentaire"]) :
            df.loc[ind, "categorie"] = find_category(df.iloc[ind], com)
        df_depences = df[df["montant"].astype("float") < 0]
        df_depences["montant"] = df_depences["montant"].astype("float").abs() 
        df_revenus  = df[df["montant"].astype("float") > 0]
        return df_depences, df_revenus


