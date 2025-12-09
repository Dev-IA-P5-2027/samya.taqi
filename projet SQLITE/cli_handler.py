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
        
    def menu_agregation_auto():
        pass #(int, text,float)
    def  menu_sql_libre():
        pass 


