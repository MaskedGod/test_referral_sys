import random, string


def generate_verification_code():
    return str(random.randint(1000, 9999))


def generate_invite_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))
