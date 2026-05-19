import hashlib
import secrets


def hash_password(password: str) -> str:
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), 100_000
    )
    return f"{pwd_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), 100_000
    )
    return secrets.compare_digest(candidate.hex(), stored_hash)
