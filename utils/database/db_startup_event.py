# import psycopg2


# Commenting for good practice
# def on_startup():
#     conn = psycopg2.connect(host = 'localhost', user = 'postgres', port = 3306)
#     with open('./SQL Scripts/create_db.sql') as file:
#         conn.cursor().execute(file.read())
