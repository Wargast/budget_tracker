from oauth2client.service_account import ServiceAccountCredentials
import gspread 
import pandas as pd
import numpy as np
import locale
import re
from pprint import pprint
from app_cli.controler import *

class Sheet_model():
    def __init__(self, scope, sheet_name):
        ### Init de la connexion a gsheet
        #try :
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "gs_credentials.json",
            scope
        )
        client = gspread.authorize(credentials)
        self.sheet = client.open(sheet_name)
        ws_db = self.sheet.worksheet("BDD_cat")
        self.cat_bdd = ws_db.get_all_values()
        ws_template = self.sheet.worksheet("Template")
        self.categories = np.array(ws_template.batch_get(['T37:T56']))[0, :,0]
        #pprint(self.cat_bdd)
        #except :
        #    print("no credentials provide")
        # share only if sheet doesn't already exist TODO
        # self.sheet.share("luc.baudinaud86@gmail.com", perm_type='user', role='writer')

    @classmethod 
    def online(cls):
        pass

    def duplicate_month_template(self, month, year):
        worksheet_template = self.sheet.worksheet("Template")
        ws = worksheet_template.duplicate(
            insert_sheet_index=len(self.sheet.worksheets()), 
            new_sheet_name= " ".join([month, year])
        )
        return ws

    def find_category(self, commentaire:str) -> str :
        """
            return the most likely category of corresponding to the 
            desciption:
            Input : desciption (string)
            Output : the categorie (string) or None if no match found 
        """
        # get the database
        for key, categorie in self.cat_bdd:
            if re.search(key.lower(), commentaire.lower()) is not None:
                print(f"{commentaire} is a '{categorie}' category !")
                return categorie
        print(f"{commentaire} category not found...")
        # define match criteria
        # execute it 
        return ""

    def update_from_file(self, file, month, year):
        # create or get worksheet if exist 
        try :
            ws = self.duplicate_month_template(month, str(year))
        except: 
            ws = self.sheet.worksheet(month+" "+str(year))
        
        df_depences, df_revenus = read_csv_from_bank(file)
        #df_depences, df_revenus = read_excel_from_app(file)
        data_list = df_depences.iloc[:, 0:4].values.tolist()
        ws.update(f'G11:J{11+len(data_list)}', data_list)
        
        data_list = df_revenus.iloc[:, 0:4].values.tolist()
        ws.update(f'B11:E{11+len(data_list)}', data_list)
        
        print("updated !! ")


if __name__=="__main__" :
    # TODO make CLI to get url and type of separator (maybe categories 
    # completion)
    print("----------- Sheet tools in degug mode ---------")
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    sh = Sheet_model(scope,"BudgetTracker")
    # sh.update_from_file("data/novembre.xlsx","TEST", 2023)
    # sh.update_from_file("data/banque_test.csv","TEST", 2023)
    depense, _ = read_csv_from_bank("data/banque_test.csv")
        

