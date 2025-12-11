from db_search import Databasearcher as data
from cli_handler import CLIHandler as cli
database=data("chinook.db")
                        
choix1=cli.menu_exploration_base()
if choix1== "A":
    choix2=cli.exploration_base()
    if choix2==1:
        table=database.lister_tables()
        print(table)
    elif choix2==2:
        nom_table=cli.decrire_table()
        colonnes=database.lister_colonnes(nom_table)
        print(colonnes)
    else :
        choix3=cli.premieres_lignes()
        print(choix3)
        lignes=database.afficher_lignes(choix3[0],choix3[1])
        print(lignes)
elif choix1=="B":
    choix2=cli.menu_agregation_auto()
    type=database.recupercation_type(choix2[0],choix2[1])
    if type=="INTEGER":
        min=database.agregation_min(choix2[0],choix2[1])
        max=database.agregation_max(choix2[0],choix2[1])
        avg=database.agregation_avg(choix2[0],choix2[1])
        sum=database.agregation_sum(choix2[0],choix2[1])
        print(f"min= {min}, max= {max},avg= {avg:.2f}, sum= {sum}")
    elif type=="FLOAT" or type== "REAL" :
        min=database.agregation_min(choix2[0],choix2[1])
        max=database.agregation_max(choix2[0],choix2[1])
        avg=database.agregation_avg(choix2[0],choix2[1])
        print(f"min= {min}, max= {max},avg= {avg:.2f}")
    elif type=='TEXT' or type=="NVARCHAR(40)" :
        pass