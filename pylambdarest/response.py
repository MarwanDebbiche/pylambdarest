import json


class Response:
    def __init__(self, code, body=None, headers=None):
        if type(code) != int:
            raise ValueError(f"Invalid code. {code} is not of type int")
        if type(headers) not in [type(None), dict]:
            raise ValueError(f"Invalid headers. {headers} is not of NoneType, dict")
        self.code = code
        self.body = body
        self.headers = headers

    def format(self):
        """
        Format the Response instance to the
        expected Lambda response format.
        """
        response = {
            "statusCode": self.code
        }

        if self.body is not None:
            response["body"] = json.dumps(self.body)

        if self.headers is not None:
            response["headers"] = self.headers

        return response
