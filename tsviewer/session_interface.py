from flask.sessions import SecureCookieSessionInterface
from typing import TYPE_CHECKING
from hashlib import sha512

if TYPE_CHECKING:
    from hashlib import _Hash


class TsViewerSecureCookieSessionInterface(SecureCookieSessionInterface):
    """
    This class still uses Flask default implementation for Session-Cookies, but the digest method
    from `hashlib.sha1` was upgrade to `hashlib.sha512` and a custom salt value enforced
    """

    def __init__(self, salt: str, *args, **kwargs) -> None:
        """
        :param salt: The salt that is used for signing Session-Cookies
        """
        super().__init__(*args, **kwargs)
        if salt is None:
            raise SaltNotSetException('Salt was not set, can\'t instantiate TsViewerSecureCookieSessionInterface')
        self.salt = salt

    @staticmethod
    def digest_method(string: bytes = b'') -> '_Hash':
        return sha512(string)


class SaltNotSetException(BaseException):
    pass
