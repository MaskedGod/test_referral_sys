import time
import random, string


SERVICE_START_TIME = time.time()


def get_uptime():
    """
    Returns the system's uptime in hours, minutes, and seconds.
    """
    uptime = time.time() - SERVICE_START_TIME
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"


def generate_verification_code():
    """Returns 4 digits long code for verification"""
    time.sleep(1.7)
    return str(random.randint(1000, 9999))


def generate_invite_code():
    "Returns 6 characters long code formed from digits and letters"
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))
