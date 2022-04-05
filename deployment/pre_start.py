import logging
import os
import time
from urllib.parse import urlparse

import psycopg2
from redis import Redis


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60
wait_seconds = 2


def check_connection(connection_func):
    current_error = None
    for _ in range(max_tries):
        try:
            if connection_func():
                break
        except Exception as e:
            time.sleep(wait_seconds)
            current_error = e
    else:
        raise current_error


def redis_test():
    redis = Redis.from_url(os.getenv("REDIS_URI"))

    try:
        redis.ping()
        return True
    except:
        return False


def postgres_test():
    try:
        conn = psycopg2.connect(os.getenv("POSTGRES_ALEMBIC_URI"))
        conn.close()
        return True
    except:
        return False


if __name__ == "__main__":
    check_connection(postgres_test)
    check_connection(redis_test)
    logger.info("Pre-start checks passed")
