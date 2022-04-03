import logging
import time

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


def test_connection():
    return True


if __name__ == "__main__":
    check_connection(test_connection)
    logger.info("Pre-start checks passed")
