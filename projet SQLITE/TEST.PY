# requete_utilisateur=input("Entre une requête SQL (SELECT uniquement): ")
# print(requete_utilisateur.split())
import sqlite3
from db_search import Databasearcher
database=Databasearcher("chinook.db")
menu="""Choisissez une option:
    1: Ajouter un élément
    2: Enlever un élément
    3: Afficher la liste
    4: Vider la liste
    5: Sauvegarder la liste
    6: Quitter
    """
print(menu)

