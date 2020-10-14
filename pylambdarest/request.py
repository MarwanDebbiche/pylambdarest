"""
Request
-------
Information parsed from the API Gateway event.

"""

import json
from typing import Optional


class Request:
    """
    Request objects created in @route handlers, and accessible
    from within the handler as the "request" argument.
    It contains parsed information about the API Gateway event.

    Parameters
    ----------
    event : dict
        The API Gateway event.

    """

    def __init__(self, event: dict):
        if not isinstance(event, dict):
            raise TypeError(f"Invalid event. {type(event)} is not dict.")
        self.event = event

    @property
    def body(self):
        """
        Return the raw body field of the API Gateway event.

        Examples
        --------
        >>> event = {"body": '{"name": "John Doe"}'}
        >>> Request(event).body
        '{"name": "John Doe"}'
        """
        return self._get_event_key("body", none_as_empty=False)

    @property
    def json(self) -> Optional[dict]:
        """
        Return a dict parsed from the body field of the API Gateway event.

        Examples
        --------
        >>> event = {"body": '{"name": "John Doe"}'}
        >>> Request(event).json["name"]
        'John Doe'
        """
        if self.body is not None:
            return json.loads(self.body)

        return None

    @property
    def path_params(self) -> Optional[dict]:
        """
        Return the pathParameters field of the API Gateway event.

        Examples
        --------
        >>> event = {"pathParameters": {"user_id": 123}}
        >>> Request(event).path_params
        {'user_id': 123}
        """
        return self._get_event_key("pathParameters")

    @property
    def query_params(self) -> Optional[dict]:
        """
        Return the queryStringParameters field of the API Gateway event.

        Examples
        --------
        >>> event = {"queryStringParameters": {"page": "3"}}
        >>> Request(event).query_params
        {'page': '3'}
        """
        return self._get_event_key("queryStringParameters")

    @property
    def method(self) -> str:
        """
        Return the request's HTTP method.

        Examples
        --------
        >>> event = {"httpMethod": "GET"}
        >>> Request(event).method
        'GET'
        """
        return self.event["httpMethod"]

    @property
    def headers(self) -> dict:
        """
        Return the request's headers.

        Examples
        --------
        >>> event = {"headers": {"accept": "*/*"}}
        >>> Request(event).headers
        {'accept': '*/*'}
        """
        return self.event["headers"]

    def _get_event_key(
        self, key: str, none_as_empty: bool = True
    ) -> Optional[dict]:
        """
        Get specific key from event object.
        """
        value = self.event.get(key)
        if value is None and none_as_empty:
            return {}

        return value
