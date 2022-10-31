"""
Route
-----
API Gateway -> Lambda handler.

"""

from collections.abc import Callable
from inspect import getfullargspec
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, ValidationError
import simplejson as json

from pylambdarest.request import Request


class route:  # pylint: disable=C0103,R0903
    """
    Lambda handler decorator.

    The @route decorator automatically format the response
    from an handler into the expected API Gateway + Lambda format.
    It also parses API Gateway's events into a Request object
    available as a "request" argument, and optionally provides
    body and query string parameters schema validation.


    Parameters
    ----------
    body_schema : dict
        Optional jsonschema for the request's body.
        If the body does not match the provided body_schema,
        the request will result in a 400 code.
        For jsonschema specification, please see
        `here <https://github.com/Julian/jsonschema>`_.

    query_params_schema : dict
        Optional jsonschema for the query string parameters.
        If the query string parameters does not match
        the provided query_params_schema, the request will
        result in a 400 code.

    Examples
    --------
    Define a 'hello' handler with body schema.
    A request argument (Request object) can be used in the handler.

    >>> user_schema = {
    ...     "type": "object",
    ...     "properties": {
    ...         "name": {"type": "string"}
    ...     },
    ...     "required": ["name"],
    ...     "additionalProperties": False
    ... }

    >>> @route(body_schema=user_schema)
    ... def hello(request):
    ...     name = request.json["name"]
    ...     return 200, {"message" : f"Hello {name} !"}

    >>> hello({"body": '{"name": "John Doe"}'}, {})
    {'statusCode': 200, 'body': '{"message": "Hello John Doe !"}'}

    If the request's body does not match the schema, a 400 will be sent.

    >>> hello({"body": '{}'}, {})
    {'statusCode': 400, 'body': '"\'name\' is a required property"'}

    You can define a query_params_schema in the same way as body_schema
    for query string parameters validation.
    """

    def __init__(
        self,
        body_model: Optional[Type[BaseModel]] = None,
        query_params_model: Optional[Type[BaseModel]] = None,
        response_model: Optional[Type[BaseModel]] = None,
    ):

        self.body_model: Optional[Type[BaseModel]] = body_model
        self.query_params_model: Optional[Type[BaseModel]] = query_params_model
        self.response_model: Optional[Type[BaseModel]] = response_model

    def __call__(self, handler, *args, **kwargs) -> Callable:
        handler_args = getfullargspec(handler).args

        def inner_func(event, context) -> dict:

            func_args_values: dict = {}
            request: Request = Request(event)
            validation_error = self._validate_request(request)
            if validation_error is not None:
                return route._format_response(
                    400, str(validation_error).split("\n", maxsplit=1)[0]
                )

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

            res = handler(**func_args_values)
            if not isinstance(res, tuple):
                res = (res,)

            return route._format_response(*res)

        return inner_func

    def _validate_request(self, request: Request) -> Optional[str]:
        try:
            if self.body_model is not None:
                if isinstance(request.json, list):
                    self.body_model(request.json)

                elif isinstance(request.json, dict):
                    self.body_model(**request.json)
                else:
                    return f"Unexpected body: {json.dumps(request.json)}"

            if self.query_params_model is not None:
                self.query_params_model(**request.query_params)

        except ValidationError as err:
            first_error = err.errors()[0]
            first_error_loc = ".".join(
                [str(loc_elem) for loc_elem in first_error["loc"]]
            )
            first_error_message = first_error["msg"]

            error_message = f"{first_error_loc}: {first_error_message}"

            return error_message

        return None

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
