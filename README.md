# pylambdarest

pylambdarest is a lightweight framework for building REST API using AWS Lambda + API Gateway.

Unlike most of other Python frameworks, it does not provide any routing capability. The routing should be handled by API Gateway itself.

Basically, it provides a `@route` decorator to parse the API Gateway event into a `Request` object accessible from the handler function as an argument. It also formats the handler's output to the expected Lambda + API Gateway format seamlessly.

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
from pylambdarest import route

@route()
def handler(request):
    body = request.json
    query_params = request.query_params
    path_params = request.path_params

    return 200, {"message": f"Hello from AWS Lambda {body['name']}!!"}
```


You can still access the original `event` and `context` arguments from the handler:

```python
from pylambdarest import route

@route()
def handler(request, event, context):
    print(event)
    print(context)
    body = request.json
    params = request.params

    return 200, {"message": f"Hello from AWS Lambda {body['name']}!!"}
```

<br/>

Path parameters defined in API Gateway can also be accessed directly as function argument:

<br/>

![api-gateway-path-params](https://raw.githubusercontent.com/MarwanDebbiche/pylambdarest/master/images/api-gateway-path-params.png)

```python
from pylambdarest import route

@route()
def get_user(user_id):
    print(user_id)

    # get user from db
    user = {"id": user_id, "name": "John Doe"}

    return 200, user
```

## Schema Validation

pylambdarest also provides basic schema validation using [jsonschema](https://github.com/Julian/jsonschema):

```python
from pylambdarest import route

user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}
    },
    "required": ["name"],
    "additionalProperties": False
}

@route(body_schema=user_schema)
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

@route(query_params_schema=query_params_schema)
def get_users(request):
    page = int(request.query_params.get("page", 1))

    # request users in db
    users = [
        {"userId": i}
        for i in range((page - 1) * 50, page * 50)
    ]

    return 200, users
```

## Motivation

Why another framework ?

When using API Gateway and python Lambdas, the most common pattern is to have one unique Lambda triggered by a **proxy** API Gateway resource. The Lambda then uses a framework like Flask to do all the routing. In an API Gateway + Lambda context, I feel like the routing should be handled by API Gateway itself, then forwarding the request to specific Lambda functions for each resource or endoint.

N.B: I find it useful to declare the API Gateway -> Lambda routing using the amazing [serverless](https://www.serverless.com/) framework

## Installation

You can install pylambdarest using pip:

```
pip install pylambdarest
```

pylambdarest should also be included in the deployment package of your Lambdas. If you use the serverless framework to manage your deployment, this can be done easily using the [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements) plugin.

To speed-up your API development, I also recommend using the [serverless-offline](https://github.com/dherault/serverless-offline) plugin.

You can look at the [sample](https://github.com/MarwanDebbiche/pylambdarest/tree/master/sample) to have a working example of this set-up.
