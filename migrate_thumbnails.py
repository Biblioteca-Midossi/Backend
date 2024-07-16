import os

from Utils.Database.DbHelper import Database

with Database() as db:
    cursor = db.get_cursor()
    cursor.execute('select isbn, id_libro from libri')

    books: list[dict] = [
        {
            "isbn": row[0],
            "id_libro": row[1],
        } for row in cursor.fetchall()
    ]

    for book in books:
        try:
            old_path = f"./assets/thumbnails/{book['isbn']}.png"
            new_path = f"./assets/thumbnails/{book['id_libro']}.png"
            os.rename(old_path, new_path)
        except FileNotFoundError:
            continue


    # print(dict)

