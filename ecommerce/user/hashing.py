from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])


def get_hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return password_context.verify(plain_password, hash_password)
