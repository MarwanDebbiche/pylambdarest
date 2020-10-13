"""
Route
-----
API Gateway -> Lambda handler.

"""

from inspect import getfullargspec
from typing import Optional

from jsonschema.validators import Draft7Validator
from jsonschema.exceptions import ValidationError

from pylambdarest.request import Request
from pylambdarest.response import Response


class route:
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
        For jsonschma specification, please see `here
        <https://github.com/Julian/jsonschema>_.`

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

    _ROUTE_ARGS = ["event", "context", "request"]

    def __init__(
        self,
        body_schema: Optional[dict] = None,
        query_params_schema: Optional[dict] = None,
    ):
        self.body_schema = body_schema
        self.query_params_schema = query_params_schema

        if self.body_schema is not None:
            self.body_schema_validator = Draft7Validator(body_schema)

        if self.query_params_schema is not None:
            self.query_params_schema_validator = Draft7Validator(
                query_params_schema
            )

    def __call__(self, function, *args, **kwargs):
        function_args = getfullargspec(function).args

        def inner_func(event, context):

            func_args_values = {}
            request = Request(event)
            validation_error = self._validate_request(request)
            if validation_error is not None:
                return Response(
                    400, str(validation_error).split("\n")[0]
                ).format()

            for arg in function_args:
                if arg in request.path_params:
                    func_args_values[arg] = request.path_params.get(arg)
                elif arg not in self._ROUTE_ARGS:
                    raise ValueError(f"Unexpected route argument {arg}")
                else:
                    func_args_values[arg] = eval(arg)

            res = function(**func_args_values)
            if not isinstance(res, tuple):
                res = (res,)

            return Response(*res).format()

        return inner_func

    def _validate_request(self, request: Request) -> Optional[str]:
        try:
            if self.body_schema is not None:
                self.body_schema_validator.validate(request.json)

            if self.query_params_schema is not None:
                self.query_params_schema_validator.validate(
                    request.query_params
                )

        except ValidationError as err:
            return str(err).split("\n")[0]

        return None
