import psycopg2


def on_startup():
    conn = psycopg2.connect(host = 'localhost', user = 'postgres', port = 3306)
    with open('./SQL Scripts/create_db.sql') as file:
        # print(file.read())
        conn.cursor().execute(file.read())
