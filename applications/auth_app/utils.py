import base64
import json
import uuid
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError

from applications.auth_app.models import User


def encode_verification_code(user: User, expire_hours: int) -> str:
    created_at = datetime.utcnow().replace(microsecond=0)
    expire_at = created_at + timedelta(hours=expire_hours)
    data = {"created_at": created_at,
            "expire_at": expire_at,
            "user_id": user.id,
            "email": user.email,
            "key": uuid.uuid4()}
    json_data = json.dumps(data, default=str)
    return base64.b64encode(json_data.encode('utf-8')).decode('utf-8')


def decode_verification_code(verification_code: str) -> dict:
    try:
        return json.loads(base64.b64decode(verification_code.encode('utf-8')))
    except (ValueError, TypeError):
        raise ValidationError("The token you are passing is invalid. "
                              "Please, request another one to reset your password")
