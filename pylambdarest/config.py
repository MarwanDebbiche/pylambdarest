# pylint: disable=C0103
"""
Config
------
Config object passed stored in App.

"""


from enum import Enum
from typing import List, Optional, Union

from pylambdarest.exceptions import ConfigError


class AuthSchemeEnum(Enum):
    """
    Enumeration of the availables authentication schemes.
    """

    JWT_BEARER = "JWT_BEARER"


class AppConfig:  # pylint: disable=R0903
    """
    Store the application confifuration.

    """

    def __init__(  # pylint: disable=R0913
        self,
        AUTH_SCHEME: Optional[AuthSchemeEnum] = None,
        JWT_SECRET: Optional[str] = None,
        JWT_ALGORITHM: Optional[str] = None,
        ALLOW_CORS: bool = False,
        CORS_ORIGIN: Optional[Union[str, List[str]]] = None,
        CORS_ALLOW_CREDENTIALS: Optional[bool] = None,
        has_jwt: Optional[bool] = None,
    ) -> None:
        self.AUTH_SCHEME: Optional[AuthSchemeEnum] = AUTH_SCHEME
        self.JWT_SECRET: Optional[str] = JWT_SECRET
        self.JWT_ALGORITHM: Optional[str] = JWT_ALGORITHM
        self.ALLOW_CORS: bool = ALLOW_CORS
        self.CORS_ORIGIN: Optional[Union[str, List[str]]] = CORS_ORIGIN
        self.CORS_ALLOW_CREDENTIALS: Optional[bool] = CORS_ALLOW_CREDENTIALS

        if (self.AUTH_SCHEME == "JWT_BEARER") and (self.JWT_SECRET is None):
            raise ConfigError(
                "JWT_SECRET cannot be none if AUTH_SCHEME = 'JWT_BEARER'"
            )
        if self.AUTH_SCHEME == "JWT_BEARER":
            if has_jwt is False:
                raise ImportError(
                    "PyJWT should be installed when using "
                    "JWT_BEARER authentication scheme"
                )
            if self.JWT_ALGORITHM is None:
                self.JWT_ALGORITHM = "HS256"

        if (self.ALLOW_CORS) and (self.CORS_ORIGIN is None):
            raise ConfigError(
                "CORS_ORIGIN cannot be none if ALLOW_CORS is True. "
                "To allow all origins, set CORS_ORIGIN to '*'"
            )

        if self.ALLOW_CORS and self.CORS_ALLOW_CREDENTIALS is None:
            self.CORS_ALLOW_CREDENTIALS = False
