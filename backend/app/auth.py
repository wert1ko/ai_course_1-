import bcrypt
from itsdangerous import URLSafeTimedSerializer
import os

SECRET_KEY = os.getenv("SECRET_KEY", "prelegal-dev-secret-change-in-prod")
SIGNER = URLSafeTimedSerializer(SECRET_KEY)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_session_token(user_id: int) -> str:
    return SIGNER.dumps({"user_id": user_id})


def get_user_from_token(token: str) -> int | None:
    try:
        data = SIGNER.loads(token, max_age=60 * 60 * 24 * 7)  # 7 days
        return data.get("user_id")
    except Exception:
        return None
