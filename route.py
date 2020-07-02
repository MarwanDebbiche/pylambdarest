from inspect import getargspec
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

from request import Request
from response import Response


class route:
    _ROUTE_ARGS = [
        "event", "context", "request"
    ]

    def __init__(self, body_schema=None):
        self.body_schema = body_schema

    def __call__(self, function, *args, **kwargs):
        function_args = getargspec(function).args

        def inner_func(event, context):
            try:
                for arg in function_args:
                    if arg not in self._ROUTE_ARGS:
                        raise ValueError(f"Unexpected route argument {arg}")

                func_args_values = {}
                request = Request(event)

                if self.body_schema is not None:
                    validate(request.json, self.body_schema)

                if 'event' in function_args:
                    func_args_values['event'] = event
                if 'context' in function_args:
                    func_args_values['context'] = context
                if 'request' in function_args:
                    func_args_values["request"] = request

                return Response(*function(**func_args_values)).format()

            except ValidationError as e:
                return Response(400, str(e).split("\n")[0]).format()
            except SchemaError as e:
                print(e)
                return Response(500, str(e).split("\n")[0]).format()
            except Exception as e:
                return Response(500, str(e)).format()

        return inner_func


if __name__ == "__main__":
    route = route(lambda a, b : a+b)
