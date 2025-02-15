from Routes.models.auth_models import UserForm
from utils.database.db_helper import PSQLDatabase


def check_user_exists(username: str, email: str) -> bool:
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        cursor.execute(
            'select * from utenti where username = %s or email = %s',
            (username, email)
        )
        return True if cursor.fetchone() is not None else False


def create_user(user: UserForm, hashed_password):
    id_istituto_map: dict = {'EXT': 0, 'ITT': 1, 'LAC': 2, 'LAV': 3}

    if not str(user.istituto).isnumeric():
        id_istituto = id_istituto_map.get(user.istituto.upper())
    else:
        id_istituto = user.istituto

    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        cursor.execute(
            'insert into utenti(nome, cognome, username, email, password, id_istituto, ruolo) '
            'values(%s, %s, %s, %s, %s, %s, %s)',
            (user.nome, user.cognome, user.username, user.email,
             hashed_password, id_istituto, 1)
        )
        db.commit()


async def get_user_profile(user_id: int):
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        cursor.execute(
            'select * from utenti where id_utente = %s',
            (user_id,)
        )
        return db.fetchone_to_dict()


async def get_user_by_id(user_id: int):
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        cursor.execute("""
            select id_utente, username, id_istituto, ruolo
            from utenti
            where id_utente = %s
        """, (user_id,))
        return db.fetchone_to_dict()


async def update_user_profile(user_id: int, profile_data: dict):
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        update_fields = ', '.join([f"{k} = %s" for k in profile_data.keys()])
        query = f"update utenti set {update_fields} where id_utente = %s"

        values = list(profile_data.values()) + [user_id]
        cursor.execute(query, values)
        db.commit()
