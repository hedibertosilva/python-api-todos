# pylint: disable=import-outside-toplevel
"""
    Provides Token class.
"""
from datetime import datetime
from datetime import timedelta
from jwt import encode
from jwt import decode


class Token:
    """ Provides tools and informations about token context.

    Attributes:
        _token (str): Token generated.
        _type (str): Token type. Defaults to "Bearer".
        _expires_at (str): Datetime that token generated will be expired.
    """

    _token: str = ""
    _type: str = "Bearer"
    _expires_at: str = ""

    def encoding(self, user_id: int) -> str:
        """ Returns token in string format.

        Args:
            user_id (int): User ID.

        Returns:
            str: Token decoded in UTF-8.
        """
        from flask import current_app as app

        self._expires_at = str(datetime.utcnow() + timedelta(hours=24))
        token_in_bytes = encode({
            "id": user_id,
            "expires_at": self._expires_at
        }, app.config['SECRET_KEY'])
        self._token = token_in_bytes.decode("UTF-8")

    @classmethod
    def decoding(cls, btoken: str) -> dict:
        """ Decoding Bearer Token.

        Args:
            btoken (str): Bearer Token supplied.

        Returns:
            dict: Token data decoded (id, expires_at).
        """
        from flask import current_app as app

        token = cls._remove_type_from(btoken)
        return decode(token, app.config['SECRET_KEY'])

    @classmethod
    def _remove_type_from(cls, btoken: str) -> str:
        """ Removing token type from token string.

        Args:
            btoken (str): Bearer Token supplied.

        Returns:
            str: Token striped without Bearer word.
        """
        return btoken.split(cls._type)[-1].strip()

    @classmethod
    def is_valid(cls, btoken: str) -> bool:
        """ Checking if the token supplied is Bearer type.

        Args:
            btoken (str): Bearer Token supplied.

        Returns:
            bool: Returns True if is a Bearer token. If not, False.
        """
        if not btoken:
            return False
        return cls._type in btoken

    @property
    def bearer_token(self) -> str:
        """ Returns token generated in Bearer format.

        Returns:
            str: Bearer Token.
        """
        return f"{self._type} {self._token}"

    @property
    def expires_at(self) -> str:
        """ Returns expires token datetime.

        Returns:
            str: Datetime that token generated will be expired.
        """
        return self._expires_at
