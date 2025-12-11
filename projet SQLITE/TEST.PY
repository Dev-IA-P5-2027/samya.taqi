# requete_utilisateur=input("Entre une requête SQL (SELECT uniquement): ")
# print(requete_utilisateur.split())
import sqlite3
from db_search import Databasearcher
database=Databasearcher("chinook.db")
choix2=input("entrez votre choix: ")
if choix2==1 or choix2==2 or choix2==3:
            print("Retente ta chance ") 
else: print('ok)')
        
            

