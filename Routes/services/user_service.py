from Routes.models.auth_models import UserForm
from utils.database.DbHelper import PSQLDatabase


def check_user_exists(username: str, email: str) -> bool:
    with PSQLDatabase() as db:
        cursor = db.cursor()
        cursor.execute(
            'select * from utenti where username = %s or email = %s',
            (username, email)
        )
        return cursor.fetchone()[0] > 0


def create_user(user: UserForm, hashed_password):
    id_istituto_map: dict = {'EXT': 0, 'ITT': 1, 'LAC': 2, 'LAV': 3}

    if not str(user.istituto).isnumeric():
        id_istituto = id_istituto_map.get(user.istituto)
    else:
        id_istituto = user.istituto

    with PSQLDatabase() as db:
        cursor = db.cursor()
        cursor.execute(
            'insert into utenti(nome, cognome, username, email, password, id_istituto, ruolo) '
            'values(%s, %s, %s, %s, %s, %s, %s)',
            (user.nome, user.cognome, user.username, user.email,
             hashed_password, id_istituto, 0)
        )
        db.commit()
