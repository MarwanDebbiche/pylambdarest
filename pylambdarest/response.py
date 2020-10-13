"""
Response
--------
Validation and Formatting of handler's response
to the expected API Gateway response format.

"""

import json
from typing import Optional, Dict, Any


class Response:
    """
    Internal Response object created in a @route handler.

    Response objects are responsible for the formatting
    of the response to the expected Lambda response format.

    Parameters
    ----------
    code : int
        Response HTTP status code.
    body : Any
        Response body. Must be JSON serializable.
    headers : dict
        Response headers.

    Examples
    --------
    >>> response = Response(200, {"message": "Hello From pylamndarest!"})
    >>> response.format()
    {'statusCode': 200, 'body': '{"message": "Hello John Doe !"}'}
    """

    def __init__(
        self,
        code: int,
        body: Optional[Any] = None,
        headers: Optional[dict] = None,
    ) -> None:
        if not isinstance(code, int):
            raise TypeError(f"Invalid status code. {type(code)} is not int.")
        if type(headers) not in [type(None), dict]:
            raise TypeError(
                f"Invalid headers. {type(headers)} is not in [NoneType, dict]."
            )
        self.code = code
        self.body = body
        self.headers = headers

    def format(self) -> Dict[str, Any]:
        """
        Format the Response instance to the expected Lambda response format.

        Examples
        --------
        >>> res = Response(200, {"message": "Hello from pylambdarest !"})
        >>> res.format()
        {'statusCode': 200, 'body': '{"message": "Hello from pylambdarest !"}'}
        """
        response: Dict[str, Any] = {"statusCode": self.code}

        if self.body is not None:
            response["body"] = json.dumps(self.body)

        if self.headers is not None:
            response["headers"] = self.headers

        return response
