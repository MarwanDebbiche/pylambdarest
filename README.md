# pylambdarest

[![CI/CD Status](https://github.com/MarwanDebbiche/pylambdarest/workflows/CI%2FCD/badge.svg?branch=master)](https://github.com/MarwanDebbiche/pylambdarest/actions?query=branch:master)
[![Coverage Status](https://coveralls.io/repos/github/MarwanDebbiche/pylambdarest/badge.svg?branch=master)](https://coveralls.io/github/MarwanDebbiche/pylambdarest?branch=master)
[![Latest Version](https://img.shields.io/pypi/v/pylambdarest.svg?color=blue)](https://pypi.python.org/pypi/pylambdarest)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pylambdarest?label=pypi%20downloads)](https://pypi.org/project/pylambdarest/)
![License](https://img.shields.io/github/license/MarwanDebbiche/pylambdarest)

pylambdarest is a lightweight opinionated framework for building REST API using [AWS Lambda](https://aws.amazon.com/lambda/) and [API Gateway](https://aws.amazon.com/api-gateway/).

## Motivation

Why another framework ?

When using API Gateway and python Lambda functions, one common pattern is to have a unique Lambda function triggered by a proxy API Gateway resource. The Lambda then uses a framework like [Flask](https://flask.palletsprojects.com/en/1.1.x/) to do all the routing. In an API Gateway + Lambda context, I feel like **the routing should be handled by API Gateway itself**, then forwarding the request to specific Lambda functions for each resource or endpoint.

## Features

- No routing. Yes, this is a feature. Routing should be handled by API Gateway.
- API Gateway event parsing (including request body and path parameters).
- Cleaner syntax.
- Optional body schema and query parameters validation.
- Optional authentication using JWT Bearet token.

## Installation

Install the package from PyPI using pip:

```
$ pip install pylambdarest
```

pylambdarest should also be included in the deployment package of your Lambda functions.

## Getting started

pylambdarest provides a `@route` decorator to parse the API Gateway event into a `Request` object available in the handler function as an argument. It also formats the handler's output to the expected Lambda + API Gateway format seamlessly.

Turning this:

```python
import json

def handler(event, context):
    body = json.loads(event["body"])
    query_params = event["queryStringParameters"]
    path_params = event["pathParameters"]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Hello from AWS Lambda {body['name']}!!"
        })
    }

```

Into this:

```python
from pylambdarest import App

app = App()

@app.route()
def handler(request):
    body = request.json
    query_params = request.query_params
    path_params = request.path_params

    return 200, {"message": f"Hello from AWS Lambda {body['name']}!!"}
```

You can still access the original `event` and `context` arguments from the handler:

```python
@app.route()
def handler(request, event, context):
    print(event)
    body = request.json

    return 200, {"message": f"Hello from AWS Lambda {body['name']}!!"}
```

<br/>

Path parameters defined in API Gateway can also be accessed directly as function argument:

<br/>

![api-gateway-path-params](https://raw.githubusercontent.com/MarwanDebbiche/pylambdarest/master/images/api-gateway-path-params.png)

```python
@app.route()
def get_user(user_id):
    print(user_id)

    # get user from db
    user = {"id": user_id, "name": "John Doe"}

    return 200, user
```

## Schema Validation

pylambdarest optionally provides schema validation using [jsonschema](https://github.com/Julian/jsonschema):

```python
user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}
    },
    "required": ["name"],
    "additionalProperties": False
}

@app.route(body_schema=user_schema)
def create_user(request):
    # If the request's body does not
    # satisfy the user_schema,
    # a 400 will be returned

    # Create user here

    return 201


query_params_schema = {
    "type": "object",
    "properties": {
        # Only string types are allowed for query parameters.
        # Types casting should be done in the handler.
        "page": {"type": "string"}
    },
    "additionalProperties": False
}

@app.route(query_params_schema=query_params_schema)
def get_users(request):
    page = int(request.query_params.get("page", 1))

    # request users in db
    users = [
        {"userId": i}
        for i in range((page - 1) * 50, page * 50)
    ]

    return 200, users
```

## Example

You can look at the [sample](https://github.com/MarwanDebbiche/pylambdarest/tree/master/sample) for a minimal pylambdarest API.

In this sample, we use the [serverless](https://www.serverless.com/) framework to declare the API Gateway -> Lambda routing

The packaging of the Lambda functions is done using the [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements) plugin.
