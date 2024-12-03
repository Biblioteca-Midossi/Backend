import os
from natsort import natsorted
from utils.database.DbHelper import PSQLDatabase


def migrate():
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        for file in natsorted(os.listdir("assets/thumbnails")):
            file_id = file[:-4]
            new_path = os.path.join("assets/thumbnails", file)
            print(new_path)
            cursor.execute("BEGIN; update libri set thumbnail_path = %s "
                           "where id_libro = %s",
                           (new_path, file_id))
            cursor.execute("select thumbnail_path from libri "
                           "where id_libro = %s "
                           "order by id_libro;",
                           (file_id,))
            db.commit()
            print(cursor.fetchall())


if __name__ == '__main__':
    migrate()
