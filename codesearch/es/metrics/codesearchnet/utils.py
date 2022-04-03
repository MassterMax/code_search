import logging
import time

logger = logging.getLogger(__name__)


def timer(func):
    def wrapper():
        start = time.time()
        func()
        logger.info(f"Execution time: {time.time() - start}s")

    return wrapper
