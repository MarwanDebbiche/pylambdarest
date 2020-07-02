import json


class Request:
    def __init__(self, event):
        self.event = event

    @property
    def body(self):
        return self.event["body"]

    @property
    def json(self):
        if self.event["body"] is not None:
            return json.loads(self.event["body"])

        return None

    @property
    def path_params(self):
        return self.event["pathParameters"]

    @property
    def query_params(self):
        return self.event["queryStringParameters"]

    @property
    def method(self):
        return self.event["httpMethod"]

    @property
    def headers(self):
        return self.event["headers"]
