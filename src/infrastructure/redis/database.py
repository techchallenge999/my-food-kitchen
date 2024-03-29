from decouple import config

import redis


redis_url = config("REDIS_URL")
redis_port = config("REDIS_PORT")
redis_user = config("REDIS_USER")
redis_password = config("REDIS_PASSWORD")

redis_db = redis.Redis(
    host=redis_url,
    port=redis_port,
    )


def get_redis_db():
    return redis_db
