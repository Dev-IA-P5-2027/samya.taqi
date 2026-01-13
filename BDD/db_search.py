import sqlite3

class DbSearch:
    def __init__(self,db_path):
        self.connection = self.connect_db(db_path=db_path)
        self.cursor = self.create_cursor()
    def connect_db(self,db_path):
        """
        Connexion à une base SQLite existante et lecture des données d'une table.
        """
        conn = sqlite3.connect(db_path)
        print('connected')
        return conn
    
    def create_cursor(self):
        return self.connection.cursor()
    
    def get_table_name(self):
        table=self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        return table

    def search_artist_by_Id(self, artist_Id):
        artist=self.cursor.execute("SELECT name FROM artists WHERE ArtistId = ?;",(artist_Id,)).fetchone()
        return artist
    
    def get_albums_by_artist(self,artist_Id):
        albums=self.cursor.execute("SELECT title FROM albums WHERE ArtistId =?;",(artist_Id,)).fetchone()
        return albums 