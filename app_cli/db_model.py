import re
import pandas as pd
import os
import front_tools

class DataBase():
    def __init__(self):
        if os.path.isfile("datas/database.csv"):
            self.database_df = pd.read_csv("datas/database.csv")
        if os.path.isfile("datas/category_hist.csv"):
            self.category_hist = pd.read_csv(
                "datas/category_hist.csv",
                header=0 
                )
        self.category_list = [
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

    def get_likely_cat(self, com):
        return ""
    
    def add_categories(self, df):
        print("Actual categories")
        for ind, com in enumerate(df["commentaire"]) :
            df.loc[ind, "categorie"] = self.get_likely_cat(com)

        front_tools.plot_df(df)

        if input("Want to change some categories ? ") == "y":        
            for ind, com in enumerate(df["commentaire"]) :
                df.loc[ind, "categorie"] = self.ask_category(df.iloc[ind], com)

        return df
    
    def ask_category(self, transaction, com: str):
        print(transaction)
        cat_guess = transaction["categorie"]
        return front_tools.select_category(
            self.category_list,
            default_cat=cat_guess
        )
