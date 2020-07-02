from inspect import getargspec
import traceback

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

from pylambdarest.request import Request
from pylambdarest.response import Response


class route:
    _ROUTE_ARGS = [
        "event", "context", "request"
    ]

    def __init__(self, body_schema=None, query_params_schema=None):
        self.body_schema = body_schema
        self.query_params_schema = query_params_schema

    def __call__(self, function, *args, **kwargs):
        function_args = getargspec(function).args

        def inner_func(event, context):
            try:
                for arg in function_args:
                    if arg not in self._ROUTE_ARGS:
                        raise ValueError(f"Unexpected route argument {arg}")

                func_args_values = {}
                request = Request(event)

                self.validate_request(request)

                if self.body_schema is not None:
                    validate(request.json, self.body_schema)

                if 'event' in function_args:
                    func_args_values['event'] = event
                if 'context' in function_args:
                    func_args_values['context'] = context
                if 'request' in function_args:
                    func_args_values["request"] = request

                res = function(**func_args_values)
                if not isinstance(res, tuple):
                    res = (res, )

                return Response(*res).format()

            except ValidationError as e:
                return Response(400, str(e).split("\n")[0]).format()
            except SchemaError as e:
                print("SchemaError:", e)
                traceback.print_exc()
                return Response(500).format()
            except Exception as e:
                print("Error:", e)
                traceback.print_exc()
                return Response(500).format()

        return inner_func

    def validate_request(self, request):
        if self.body_schema is not None:
            validate(request.json, self.body_schema)

        if self.query_params_schema is not None:
            validate(request.query_params, self.query_params_schema)
