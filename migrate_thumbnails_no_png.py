import os

from natsort import natsorted

from utils.database.db_helper import PSQLDatabase


def migrate():
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        cursor.execute("""
            update libri
            set thumbnail_path = replace(thumbnail_path, '.png', '')
            where thumbnail_path like '%.png%'
        """)
        cursor.execute("""
            select thumbnail_path from libri
        """)
        db.commit()
        thumbnails = [item[0] for item in cursor.fetchall()]
        print(thumbnails)
        # for index, thumbnail in enumerate(thumbnails):
        #     thumbnails[index] = thumbnail.replace('.png', '')
        #     print(thumbnail.replace('.png', ''))
        # print(thumbnails)


if __name__ == '__main__':
    migrate()
