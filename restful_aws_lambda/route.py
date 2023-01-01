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
    Lambda handler decorator.

    The @route decorator automatically format the response
    from a handler into the expected API Gateway + Lambda format.
    It also parses API Gateway's events into a Request object
    available as a "request" argument, and optionally provides
    body and query string parameters schema validation.

    Examples
    --------
    Define a 'hello' handler. A request argument (Request object) can be used
    in the handler.

    >>> @route()
    ... def hello(request):
    ...     name = request.json["name"]
    ...     return 200, {"message" : f"Hello {name} !"}

    >>> hello({"body": '{"name": "John Doe"}'}, {})
    {'statusCode': 200, 'body': '{"message": "Hello John Doe !"}'}
    """

    def __init__(self):
        pass

    def __call__(self, handler, *args, **kwargs) -> Callable:
        handler_args = getfullargspec(handler).args

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

            response = handler(**func_args_values)
            if not isinstance(response, tuple):
                res = (response,)

            return Route._format_response(*response)
        return inner_func

    @staticmethod
    def _format_response(
        code: int, body: Any = None, headers: Optional[dict] = None
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
            response["body"] = json.dumps(body)

        if headers is not None:
            response["headers"] = headers

        return response
