"""
decorator
-----
User-friendly @route decorator.

"""
from functools import wraps
from typing import Callable, Optional

from restful_aws_lambda.route import Route


def _double_wrap(function):
    """
    A decorator decorator, allowing the decorator to be used as:
    >>> @decorator(with, arguments, and=kwargs)
    or
    >>> @decorator
    """

    @wraps(function)
    def new_decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return function(args[0])
        return lambda real_function: function(real_function, *args, **kwargs)

    return new_decorator


@_double_wrap
def route(lambda_handler, json: Optional[dict] = None) -> Callable:
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

    >>> @route
    ... def hello(request):
    ...     name = request.json["name"]
    ...     return 200, {"message" : f"Hello {name} !"}

    >>> hello({"body": '{"name": "John Doe"}'}, {})
    {'statusCode': 200, 'body': '{"message": "Hello John Doe !"}'}
    """
    return Route(lambda_handler, json_dumps_options=json or {}).restful()
