from utils.auth.AuthHelper import create_session_cookie
from utils.database.DbHelper import RedisDatabase


def create_user_session(user_data: dict):
    session_id = create_session_cookie(user_data)

    with RedisDatabase() as redis:
        # Delete old session if exists
        if redis.client.exists(session_id):
            redis.client.delete(session_id)

        # Set new session
        redis.client.hset(session_id, mapping = user_data)
        redis.client.expire(session_id, 14400)  # 4 hours

    return session_id


def delete_user_session(session_id: str):
    with RedisDatabase() as redis:
        redis.client.delete(session_id)
