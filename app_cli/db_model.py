import re
import pandas as pd
import os
import front_tools

class DataBase():
    def __init__(self):
        self.db_path = "datas/database.csv"
        self.cat_hist_path = "datas/category_hist.csv"
        if os.path.isfile(self.db_path):
            self.database_df = pd.read_csv(self.db_path)
        if os.path.isfile(self.cat_hist_path):
            self.category_hist = pd.read_csv(
                self.cat_hist_path,
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

    def save_data(self):
        try:
            self.category_hist.to_csv(self.cat_hist_path)
        except:
            print("no hist cat file")
        try:
            self.database_df.to_csv(self.db_path)
        except:
            print("no df file")

    def get_likely_cat(self, com):
        for index, row in self.category_hist.iterrows():
            categorie = row["categorie"]
            row_com = row["commantaire"]
            if re.search(row_com.lower(), com.lower()) is not None:
                # print(f"{com} is a '{categorie}' category !")
                return categorie
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
        cat_guess = self.get_likely_cat(com)
        cat = front_tools.select_category(
            self.category_list,
            default_cat=cat_guess
        )
        last_index = len(self.category_hist)
        self.category_hist.loc[last_index] = [last_index, com, cat]
        return cat
