class CLIHandler :
    def menu_exploration_base():
        menu="""bonjour bienvenue!
        A- Exploration de la base
        B- Agrégations automatiques
        C- Requêtes SQL libres
        """
        print(menu)
        choix1=input("choisissez une catégorie et entrez la lettre correspondante: ")
        if choix1!="A" and choix1!="B" and choix1!="C":
            print("Retente ta chance ")
            
        else:
            return choix1
    def exploration_base():
        menu_expl="""
        1- lister toutes les tables
        2- Décrire une table 
        3- Afficher les premières lignes d'une table
        """
        print(menu_expl)
        choix2=int(input("entrez votre choix: "))
        if choix2!=1 and choix2!=2 and choix2!=3:
            print("Retente ta chance ") 
        else:
            return choix2
    def decrire_table():
        table=input("entrez le nom de la table: ")
        return table
    def premieres_lignes():
        nom_table=input("entre un nom de table:")
        nombres=int(input("entre le nombre de ligne que tu veux afficher:"))
        return nom_table, nombres
    def menu_agregation_auto():
        nom_table=input("entrez le nom de la table: ")
        nom_colonne=input("entrez la non de la colonne: ")
        return nom_table , nom_colonne
    
    def  menu_sql_libre():
        requete_sql=input("entre une requête SQL: ")
        return requete_sql
    

