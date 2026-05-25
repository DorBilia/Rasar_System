from passlib.context import CryptContext

import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from settings import settings

_pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    return _pwd_context.verify(password, stored_hash)

def hash_refresh_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def generate_raw_refresh_token() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("ascii").rstrip("=")


def create_access_token(*, subject: str, role_member_name: str) -> tuple[str, int]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRES_SECONDS)
    claims = {
        "iss": settings.JWT_ISS,
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "roles": [f"ROLE_{role_member_name}"],
    }
    token = jwt.encode(claims, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("ascii")
    return token, settings.ACCESS_TOKEN_EXPIRES_SECONDS


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
        options={"require": ["exp", "sub", "roles"]},
        issuer=settings.JWT_ISS,
    )
