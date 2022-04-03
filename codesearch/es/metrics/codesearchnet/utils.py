from functools import wraps
import logging
import time

logger = logging.getLogger(__name__)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        logger.info(f"total execution time: {time.time() - start}s")

    return wrapper
