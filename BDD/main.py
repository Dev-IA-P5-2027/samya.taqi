from db_search import DbSearch

chinook_db_search = DbSearch(db_path='data\chinook.db')
# chinook_cursor = chinook_db_search.cursor
# chinooksearch=DbSearch()
# chinooksearch.connect_db(db_path='..\data\chinook.db')
# print(chinooksearch.get_table_name())
table = chinook_db_search.get_table_name()
print(table)
# artist=chinook_db_search.search_artist_by_Id(5)
# print(artist)
artist_id = 3
result = chinook_db_search.search_artist_by_Id(artist_id)

if result:
    print("Nom de l'artiste :", result[0])
else:
    print("Artiste non trouvé.")

Albums=chinook_db_search.get_albums_by_artist(artist_Id=2)
print(Albums)