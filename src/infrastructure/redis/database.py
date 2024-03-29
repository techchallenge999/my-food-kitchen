from decouple import config

import redis


redis_url = config("REDIS_URL")
redis_port = config("REDIS_PORT")
redis_user = config("REDIS_USER")
redis_password = config("REDIS_PASSWORD")

r = redis.Redis(
    host=redis_url,
    port=redis_port,
    username=redis_user,
    password=redis_password,
    )


def get_session():
    return r
