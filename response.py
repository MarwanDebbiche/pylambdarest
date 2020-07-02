import json


class Response:
    def __init__(self, code, body):
        self.code = code
        self.body = body

    def format(self):
        return {
            "statusCode": self.code,
            "body": json.dumps(self.body)
        }
