"""
Route
-----
API Gateway -> Lambda handler.

"""
import json
from collections.abc import Callable
from inspect import getfullargspec
from typing import Any, Dict, Optional

from restful_aws_lambda.request import Request


class Route:  # pylint: disable=C0103,R0903
    """
    Lambda handler decorator core class.
    """

    def __init__(self, lambda_handler: Callable, json_dumps_options: dict):
        self._handler: Callable = lambda_handler
        self._json_dumps_options: dict = json_dumps_options

    def restful(self) -> Callable:
        """Build and return a restful lambda_handler."""
        handler_args = getfullargspec(self._handler).args

        def inner_func(event, context) -> dict:

            func_args_values: dict = {}
            request: Request = Request(event)

            for arg in handler_args:
                if arg in request.path_params:
                    func_args_values[arg] = request.path_params.get(arg)
                elif arg == "event":
                    func_args_values["event"] = event
                elif arg == "context":
                    func_args_values["context"] = context
                elif arg == "request":
                    func_args_values["request"] = request
                else:
                    raise TypeError(
                        f"handler got an unexpected argument '{arg}'"
                    )

            response = self._handler(**func_args_values)
            if not isinstance(response, tuple):
                response = (response,)

            return self._format_response(*response)

        return inner_func

    def _format_response(
        self, code: int, body: Any = None, headers: Optional[dict] = None
    ) -> Dict[str, Any]:
        """
        Format the handler's response to the expected Lambda response format.
        """
        if not isinstance(code, int):
            raise TypeError(f"Invalid status code. {type(code)} is not int.")
        if type(headers) not in [type(None), dict]:
            raise TypeError(
                f"Invalid headers. {type(headers)} is not in [NoneType, dict]."
            )
        response: Dict[str, Any] = {"statusCode": code}

        if body is not None:
            response["body"] = json.dumps(body, **self._json_dumps_options)

        if headers is not None:
            response["headers"] = headers

        return response
