import datetime
from functools import wraps
import logging
import subprocess
import time

logger = logging.getLogger(__name__)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        logger.warning(f"total execution time: {time.time() - start}s")
        return result
    return wrapper


def free_memory_logging(output_file):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            output = subprocess.check_output("free -m", shell=True)
            with open(output_file, "a+") as f:
                f.write(f"current time: {datetime.datetime.utcnow()}\n")
                f.writelines(output.decode("utf-8"))
                f.write("\n")
            return func(*args, **kwargs)
        return wrapper
    return inner
