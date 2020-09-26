import json


class Request:
    def __init__(self, event):
        if type(event) != dict:
            raise TypeError(f"Invalid event. {type(event)} is not dict.")
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
        return self._get_event_key("pathParameters")

    @property
    def query_params(self):
        return self._get_event_key("queryStringParameters")

    @property
    def method(self):
        return self.event["httpMethod"]

    @property
    def headers(self):
        return self.event["headers"]

    def _get_event_key(self, key, none_as_empty=True):
        value = self.event.get(key)
        if value is None and none_as_empty:
            return {}

        return value
