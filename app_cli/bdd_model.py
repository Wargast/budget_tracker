import mysql.connector
import sys

sql_create = """
CREATE TABLE IF NOT EXISTS Expences ( 
   date int(6) NOT NULL, 
   commentary varchar(100) DEFAULT NULL, 
   prix float(5,2) DEFAULT NULL, 
   PRIMARY KEY(ref), 
   CHECK (stock>=0) ); """


def add_expense(date, commentary, prix):
    try:
        conn = mysql.connector.connect(host="192.168.125.2", 
                                        user="georges", password="what-else?", 
                                        database="budget_history")

        cursor = conn.cursor()
        cursor.execute(sql_create)

        try:
            reference = (date, commentary, prix) 
            cursor.execute("""INSERT INTO Produits (ref, nom, stock, prix) VALUES(%s, %s, %s, %s)""", reference)
            
            reference = {'ref': 543154, 'nom' : "Gelée de coing 300g", 'stock' : 5, 'prix' : 3.75} 
            cursor.execute("""INSERT INTO Produits (ref, nom, stock, prix) VALUES(%(ref)d, "%(nom)s", %(stock)d, %(prix)f)""", reference)

            conn.commit()

        except:
            # En cas d'erreur on annule les modifications
            conn.rollback()

        cursor.execute("""SELECT ref, nom, prix FROM Produits WHERE stock > %d """, (0, )) 
        rows = cursor.fetchall() 
        for row in rows: 
            print('{0} : {1} - {2}'.format(row[0], row[1], row[2]))


    except mysql.connector.errors.InterfaceError as e:
        print("Error %d: %s" % (e.args[0],e.args[1]))
        sys.exit(1)


    finally:
        # On ferme la connexion
        if conn:
            conn.close()