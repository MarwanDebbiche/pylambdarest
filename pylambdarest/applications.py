"""
App
---

Application object to store the common config.

"""
from typing import Optional, Dict, Any
from inspect import getfullargspec


import simplejson as json
from jsonschema.exceptions import ValidationError  # type: ignore
from jsonschema.validators import Draft7Validator  # type: ignore

try:
    import jwt

    HAS_JWT = True
except ImportError:
    HAS_JWT = False


from pylambdarest.config import AppConfig
from pylambdarest.exceptions import AuthError
from pylambdarest.request import Request


class App:  # pylint: disable=R0903
    """
    Pylambdarest Application.
    """

    def __init__(self, config: Optional[dict] = None):
        if config is not None:
            self.config = AppConfig(**config, has_jwt=HAS_JWT)
        else:
            self.config = AppConfig()

    @staticmethod
    def _validate_request(
        request: Request,
        body_schema_validator: Draft7Validator,
        query_params_schema_validator: Draft7Validator,
    ) -> Optional[str]:
        try:
            if body_schema_validator is not None:
                body_schema_validator.validate(request.json)

            if query_params_schema_validator is not None:
                query_params_schema_validator.validate(request.query_params)

        except ValidationError as err:
            return str(err).split("\n", maxsplit=1)[0]

        return None

    def _format_response(
        self, code: int, body: Any = None, headers: Optional[dict] = None
    ) -> Dict[str, Any]:
        """
        Format the handler's response to the expected Lambda response format.
        """
        if not isinstance(code, int):
            print(code, body, headers)
            raise TypeError(f"Invalid status code. {type(code)} is not int.")
        if type(headers) not in [type(None), dict]:
            raise TypeError(
                f"Invalid headers. {type(headers)} is not in [NoneType, dict]."
            )
        response: Dict[str, Any] = {"statusCode": code}

        if body is not None:
            response["body"] = json.dumps(body)

        if self.config.ALLOW_CORS:
            response["headers"] = {
                "Access-Control-Allow-Origin": self.config.CORS_ORIGIN
            }

        if headers is not None:
            response["headers"] = {**response.get("headers", {}), **headers}

        return response

    def _check_jwt_bearer(self, request: Request):
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            raise AuthError("Empty Authorization header")

        schema: str = auth_header.split()[0]
        token: str = auth_header.split()[1]

        if schema != "Bearer":
            raise AuthError("Invalid Authorization header for Bearer auth")

        try:
            if self.config.JWT_SECRET is None:
                raise Exception(
                    "Unexpected exception JWT_SECRET should not be None"
                )
            JWT_SECRET: str = self.config.JWT_SECRET

            payload: dict = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[self.config.JWT_ALGORITHM],
            )
        except (
            jwt.InvalidSignatureError,
            jwt.DecodeError,
            jwt.ExpiredSignatureError,
        ) as exc:
            raise AuthError("Unautorized") from exc

        return payload

    def route(
        self,
        body_schema: Optional[dict] = None,
        query_params_schema: Optional[dict] = None,
        restricted: Optional[bool] = None,
    ):
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

        restricted : bool
            Whether the route is restricted or not. Can only be true if
            app config's AUTH_SCHEME is "JWT_BEARER"

        Examples
        --------
        Define a 'hello' handler with body schema.
        A request argument (Request object) can be used in the handler.

        >>> app = App()

        >>> user_schema = {
        ...     "type": "object",
        ...     "properties": {
        ...         "name": {"type": "string"}
        ...     },
        ...     "required": ["name"],
        ...     "additionalProperties": False
        ... }

        >>> @app.route(body_schema=user_schema)
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
        if restricted:
            if self.config.JWT_SECRET is None:
                raise ValueError(
                    "Cannot declare route as restricted as no JWT_SECRET was passed in app config"
                )

        body_schema_validator = (
            Draft7Validator(body_schema) if body_schema is not None else None
        )

        query_params_schema_validator = (
            Draft7Validator(query_params_schema)
            if query_params_schema is not None
            else None
        )

        def decorator(lambda_handler):
            handler_args = getfullargspec(lambda_handler).args

            def wrapper(event, context):
                func_args_values: dict = {}
                request: Request = Request(event)

                if restricted is True:
                    try:
                        jwt_payload = self._check_jwt_bearer(request)
                    except AuthError:
                        return self._format_response(401, "Unauthorized")

                validation_error = App._validate_request(
                    request,
                    body_schema_validator=body_schema_validator,
                    query_params_schema_validator=query_params_schema_validator,
                )
                if validation_error is not None:
                    return self._format_response(
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
                    elif arg == "jwt_payload":
                        if (
                            (self.config.AUTH_SCHEME != "JWT_BEARER")
                            or (restricted is None)
                            or (restricted is False)
                        ):
                            raise TypeError(
                                "handler got an unexpected argument jwt_payload"
                            )
                        func_args_values["jwt_payload"] = jwt_payload
                    else:
                        raise TypeError(
                            f"handler got an unexpected argument '{arg}'"
                        )

                res = lambda_handler(**func_args_values)
                if not isinstance(res, tuple):
                    res = (res,)

                return self._format_response(*res)

            return wrapper

        return decorator
