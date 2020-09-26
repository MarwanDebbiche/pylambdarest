import json
from typing import Optional


class Request:
    def __init__(self, event: dict):
        if type(event) != dict:
            raise TypeError(f"Invalid event. {type(event)} is not dict.")
        self.event = event

    @property
    def body(self):
        return self.event["body"]

    @property
    def json(self) -> Optional[dict]:
        if self.event["body"] is not None:
            return json.loads(self.event["body"])

        return None

    @property
    def path_params(self) -> Optional[dict]:
        return self._get_event_key("pathParameters")

    @property
    def query_params(self) -> Optional[dict]:
        return self._get_event_key("queryStringParameters")

    @property
    def method(self) -> str:
        return self.event["httpMethod"]

    @property
    def headers(self) -> dict:
        return self.event["headers"]

    def _get_event_key(
        self, key: str, none_as_empty: bool = True
    ) -> Optional[dict]:
        value = self.event.get(key)
        if value is None and none_as_empty:
            return {}

        return value
