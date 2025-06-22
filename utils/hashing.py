
import bcrypt

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def check_password(password_input: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password_input.encode(), hashed_password.encode())