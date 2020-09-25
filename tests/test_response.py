import json

import pytest

from pylambdarest import Response


def response():
    return {
        'code': 200,
        'body': {"test": "pass"},
        'headers': {'test-forwarded-for': 'user'},
    }


@pytest.fixture
def example_response():
    return Response(**response())


def test_response_is_correctly_formated(example_response):
    expected_response = {
        "statusCode": 200,
        "body": '{"test": "pass"}',
        "headers": {'test-forwarded-for': 'user'},
    }
    assert example_response.format() == expected_response


def test_response_code(example_response):
    assert example_response.code == response()["code"]


def test_response_body(example_response):
    assert example_response.body == response()["body"]


def test_response_headers(example_response):
    assert example_response.headers == response()["headers"]
