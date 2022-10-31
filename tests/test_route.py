import json

import pytest

from pylambdarest import route
from pydantic import BaseModel


@pytest.fixture
def empty_route():
    @route()
    def test_route():
        return 200

    return test_route


@pytest.fixture
def get_user_route():
    @route()
    def test_route(user_id):
        user = {"id": user_id, "name": "Test User"}
        return 200, user

    return test_route


@pytest.fixture
def invalid_code_route():
    @route()
    def invalid_code_handler():
        return "code"

    return invalid_code_handler


@pytest.fixture
def invalid_response_headers_route():
    @route()
    def invalid_response_headers_handler():
        return 200, {}, "invalid_headers"

    return invalid_response_headers_handler


@pytest.fixture
def model_validation_route():
    class BodyModel(BaseModel):
        name: str

    class QueryParamsModel(BaseModel):
        test: str

    @route(body_model=BodyModel, query_params_model=QueryParamsModel)
    def test_route():
        return 200

    return test_route


@pytest.fixture
def event_context_as_headers_route():
    @route()
    def test_route(event, context):
        return 200, {}, {"event": event, "context": context}

    return test_route


def test_status_code(empty_route):
    event = {}
    context = {}
    response = empty_route(event, context)
    assert response["statusCode"] == 200


def test_path_params(get_user_route):
    event = {"pathParameters": {"user_id": 123}}
    context = None
    response = get_user_route(event, context)
    assert response["statusCode"] == 200
    assert response["body"] == '{"id": 123, "name": "Test User"}'


def test_invalid_route_args(get_user_route):
    # test that calling the get_user_route
    # without the expected user_id in pathParameters
    # raises a TypeError
    with pytest.raises(TypeError):
        get_user_route({}, {})


def test_invalid_code(invalid_code_route):
    with pytest.raises(TypeError):
        invalid_code_route({}, {})


def test_invalid_invalid_response_headers(invalid_response_headers_route):
    with pytest.raises(TypeError):
        invalid_response_headers_route({}, {})


def test_event_context(event_context_as_headers_route):
    test_event = {"type": "test_event"}
    test_context = {"type": "test_context"}

    response = event_context_as_headers_route(test_event, test_context)

    expected_headers = {"event": test_event, "context": test_context}

    assert response["headers"] == expected_headers


def test_model_validation(model_validation_route):
    context = {}

    event = {"body": json.dumps({"invalid": "schema"})}
    response = model_validation_route(event, context)
    assert response["statusCode"] == 400

    event = {
        "body": json.dumps({"name": "Test Name"}),
        "queryStringParameters": {"invalidKey": "test"},
    }
    response = model_validation_route(event, context)
    assert response["statusCode"] == 400

    event = {
        "body": json.dumps({"name": "Test Name"}),
        "queryStringParameters": {"test": "test"},
    }
    response = model_validation_route(event, context)
    assert response["statusCode"] == 200

    class BodyModel(BaseModel):
        name: str

    @route(
        body_model=list[BodyModel],
    )
    def test_route():
        return 200

    event = {
        "body": json.dumps([{"name": "Test Name"}, {"name": "Test Name 2"}]),
    }

    response = test_route(event, context)
    assert response["statusCode"] == 200

    event = {
        "body": json.dumps(None),
    }
    response = test_route(event, context)
    assert response["statusCode"] == 400


def test_invalid_null_body():
    @route()
    def empty_route(request):
        assert request.body is None
        assert request.json is None
        return 200

    empty_route({}, {})  # pylint: disable=too-many-function-args
    empty_route({"body": None}, {})  # pylint: disable=too-many-function-args
