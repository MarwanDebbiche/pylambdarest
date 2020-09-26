import pytest

from pylambdarest import Request


def event():
    return {
        "body": '{"test":"pass"}',
        "httpMethod": "testGET",
        "headers": {"test-forwarded-for": "user"},
        "queryStringParameters": {"name": "testName", "type": "fake"},
        "pathParameters": {"key1": "value1", "key2": "value2"},
    }


@pytest.fixture
def example_request():
    return Request(event())


def test_invalid_event():
    with pytest.raises(TypeError):
        Request("invalid_event")


def test_body_is_returned(example_request):
    assert example_request.body == event()["body"]


def test_json_is_loaded(example_request):
    assert example_request.json == {"test": "pass"}


def test_json_body_can_be_none():
    assert Request({"body": None}).json is None


def test_path_params_are_returned(example_request):
    assert example_request.path_params == event()["pathParameters"]


def test_path_params_can_be_empty():
    assert Request({"pathParameters": None}).path_params == {}


def test_query_params_are_returned(example_request):
    assert example_request.query_params == event()["queryStringParameters"]


def test_query_params_can_be_empty():
    assert Request({"queryStringParameters": None}).query_params == {}


def test_method_is_returned(example_request):
    assert example_request.method == event()["httpMethod"]


def test_headers_are_returned(example_request):
    assert example_request.headers == event()["headers"]
