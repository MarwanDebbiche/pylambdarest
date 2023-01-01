# restful-aws-lambda

[![CI/CD Status](https://github.com/joffreybvn/restful-aws-lambda/workflows/CI%2FCD/badge.svg?branch=master)](https://github.com/joffreybvn/restful-aws-lambda/actions?query=branch:master)
[![Coverage Status](https://coveralls.io/repos/github/joffreybvn/restful-aws-lambda/badge.svg?branch=master)](https://coveralls.io/github/joffreybvn/restful-aws-lambda?branch=master)
[![Latest Version](https://img.shields.io/pypi/v/restful-aws-lambda.svg?color=blue)](https://pypi.python.org/pypi/restful-aws-lambda)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/restful-aws-lambda?label=pypi%20downloads)](https://pypi.org/project/restful-aws-lambda/)
![License](https://img.shields.io/github/license/joffreybvn/restful-aws-lambda)

restful-aws-lambda is a lightweight opinionated framework for building REST API using [AWS Lambda](https://aws.amazon.com/lambda/) and [API Gateway](https://aws.amazon.com/api-gateway/).

## Motivation

Why another framework ?

When using API Gateway and python Lambda functions, the most common pattern is to have a unique Lambda function triggered by a proxy API Gateway resource. The Lambda then uses a framework like [Flask](https://flask.palletsprojects.com/en/1.1.x/) to do all the routing. In an API Gateway + Lambda context, I feel like **the routing should be handled by API Gateway itself**, then forwarding the request to specific Lambda functions for each resource or endpoint.

## Features

- No routing. Yes, this is a feature. Routing should be handled by API Gateway.
- API Gateway event parsing (including request body and path parameters).
- Cleaner syntax.
- Customizable JSON dumps behavior
- No schema validation

## Installation

Install the package from PyPI using pip:

```
$ pip install restful-aws-lambda
```

restful-aws-lambda should also be included in the deployment package of your Lambda functions.

## Getting started

restful-aws-lambda provides a `@route` decorator to parse the API Gateway event into a `Request` object available in the handler function as an argument. It also formats the handler's output to the expected Lambda + API Gateway format seamlessly.

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
from restful_aws_lambda import route


@route
def handler(request):
    body = request.json
    query_params = request.query_params
    path_params = request.path_params

    return 200, {"message": f"Hello from AWS Lambda {body['name']}!!"}
```

You can still access the original `event` and `context` arguments from the handler:

```python
from restful_aws_lambda import route


@route
def handler(request, event, context):
    print(event)
    body = request.json

    return 200, {"message": f"Hello from AWS Lambda {body['name']}!!"}
```

<br/>

Path parameters defined in API Gateway can also be accessed directly as function argument:

<br/>

![api-gateway-path-params](https://raw.githubusercontent.com/joffreybvn/restful-aws-lambda/master/images/api-gateway-path-params.png)

```python
from restful_aws_lambda import route


@route
def get_user(user_id):
    print(user_id)

    # get user from db
    user = {"id": user_id, "name": "John Doe"}

    return 200, user
```

## JSON dumps options

restful-aws-lambda uses the default `json` library to dump the lambda handler response. You can customize the behavior of it by passing `json.dumps()` keyword arguments to the `json=` parameter:

```python
import json
import datetime
from restful_aws_lambda import route

class JSONDatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        return super(JSONDatetimeEncoder, self).default(obj)


@route(json={"cls": JSONDatetimeEncoder})
def lambda_handler(request):
    today = datetime.date.today()
    return 200, {"today": today}
```

## Example

You can look at the [sample](https://github.com/joffreybvn/restful-aws-lambda/tree/master/sample) for a minimal pylambdarest API.

In this sample, we use the [serverless](https://www.serverless.com/) framework to declare the API Gateway -> Lambda routing

The packaging of the Lambda functions is done using the [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements) plugin.
