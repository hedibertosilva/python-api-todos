import jwt
from datetime import datetime
from datetime import timedelta
from typing import Any, Mapping




class Token:

    _type: str = "Bearer"
    _token: str
    _expires_at: str

    def encoding(self, id: int) -> str:
        from flask import current_app as app

        self.expires_at = str(datetime.utcnow() + timedelta(hours=24))
        token_in_bytes = jwt.encode({
            "id": id,
            "expires_at": self.expires_at
        }, app.config['SECRET_KEY'])
        self._token = token_in_bytes.decode("UTF-8")

    @classmethod
    def decoding(cls, btoken: str) -> Mapping:
        from flask import current_app as app

        token = cls._remove_type_from(btoken)
        return jwt.decode(token, app.config['SECRET_KEY'])

    @classmethod
    def _remove_type_from(cls, btoken: str) -> str:
        return btoken.split(cls._type)[-1].strip()

    @classmethod
    def is_valid(cls, btoken: str) -> bool:
        if not btoken:
            return False
        return cls._type in btoken

    @property
    def bearer_token(self) -> str:
        return f"{self._type} {self._token}"

    @property
    def expire_at(self) -> str:
        return self._expires_at
