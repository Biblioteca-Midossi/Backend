from Utils.Database.DbHelper import Database

with Database() as db:
    cursor = db.cursor()
    cursor.execute('select isbn, id_libro from libri')

    print(cursor.fetchall())

