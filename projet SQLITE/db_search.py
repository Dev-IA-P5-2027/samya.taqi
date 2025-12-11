import sqlite3

class Databasearcher :
   
    def __init__(self,db_path):
        self.connection = self.connect_db(db_path=db_path)
        self.cursor = self.create_cursor()
    
    
    def connect_db(self,db_path):
        
        conn = sqlite3.connect(db_path)
        print('connected')
        return conn
    
    def create_cursor(self):
        return self.connection.cursor()
    
    def lister_tables(self):
        table=self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        return table
    
    def lister_colonnes(self,table):
        
        colonnes=self.cursor.execute(f"PRAGMA table_info({table})").fetchall()
        return colonnes    
    def afficher_lignes(self, nom_table, n):
          self.cursor.execute(f"SELECT * FROM {nom_table}")
          lignes=self.cursor.fetchmany(n)
          return lignes
                        
    
    def executer_sql(self,requete_utilisateur):
        
        liste_mots_requete=requete_utilisateur.split()
        
        if liste_mots_requete[0]== "SELECT":
            self.cursor.execute(requete_utilisateur)
            return self.cursor.fetchall()
        else : return False

    def recupercation_type(self,nom_table, nom_colonne):

        table_info=self.cursor.execute(f"PRAGMA table_info({nom_table})")
        for i in table_info:
            if i[1]== nom_colonne:
                type=i[2]
                return type
    def agregation_min(self,nom_table, nom_colonne):
               self.cursor.execute(f"SELECT MIN({nom_colonne}) FROM {nom_table}")
               Min=self.cursor.fetchall()
               return Min[0][0]
    def agregation_max(self,nom_table, nom_colonne):
               self.cursor.execute(f"SELECT MAX({nom_colonne}) FROM {nom_table}")
               Max=self.cursor.fetchall()
               return Max[0][0]
    def agregation_avg(self,nom_table, nom_colonne):
               self.cursor.execute(f"SELECT AVG({nom_colonne}) FROM {nom_table}")
               Avg=self.cursor.fetchall()
               return Avg[0][0]
    def agregation_sum(self,nom_table, nom_colonne):
               self.cursor.execute(f"SELECT SUM({nom_colonne}) FROM {nom_table}")
               Sum=self.cursor.fetchall()
               return Sum[0][0]
    def agregation_count_distinct(self,nom_table, nom_colonne):
               self.cursor.execute(f"SELECT COUNT (DISTINCT({nom_colonne})) FROM {nom_table}")
               count_distint=self.cursor.fetchall()
               return count_distint[0][0]
        
            