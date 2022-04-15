import jwt
from datetime import datetime
from datetime import timedelta
from typing import Mapping




class Token:

    type: str = "Bearer"
    token: str
    expires_at: str

    def encoding(self, id: int) -> str:
        from flask import current_app as app

        self.expires_at = str(datetime.utcnow() + timedelta(hours=24))
        token_in_bytes = jwt.encode({
            "id": id,
            "expires_at": self.expires_at
        }, app.config['SECRET_KEY'])
        self.token = token_in_bytes.decode("UTF-8")

    @classmethod
    def decoding(cls, btoken: str) -> Mapping:
        from flask import current_app as app

        token = cls._remove_type_from(btoken)
        return jwt.decode(token, app.config['SECRET_KEY'])

    @classmethod
    def _remove_type_from(cls, btoken: str) -> str:
        return btoken.split(cls.type)[-1].strip()
