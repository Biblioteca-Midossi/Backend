import mysql.connector


def on_startup():
    conn = mysql.connector.connect(host = 'localhost', user = 'root', port = 3306)
    with open('./SQL Scripts/create_db.sql') as file:
        # print(file.read())
        conn.cursor().execute(file.read())
