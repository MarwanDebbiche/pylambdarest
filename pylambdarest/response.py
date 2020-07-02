import json


class Response:
    def __init__(self, code, body=None, headers=None):
        self.code = code
        self.body = body
        self.headers = None

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
