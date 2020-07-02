# pylambdarest

pylambdarest is a lightweight framework for building REST API using AWS Lambda + API Gateway.

Unlike most of other Python frameworks, it does not provide any routing capability. The routing should be handled by API Gateway itself.

Basically, it just provide a `@route` decorator to parse the API Gateway event into a `Request` object accessible from the handler function as an argument. It also formats the handler's output to the expected lambda + API Gateway format seamlessly.

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

You can still access the original `event`, `context` argument from the handler:

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
    return 201, {}
```

## Motivation

Why another framework ?

Two reasons:

- When using API Gateway + python lambdas, the pattern I often see is one unique lambda triggered by a **proxy API Gateway resource**. The lambda then uses Flask to do all the routing. In an API Gateway + Lambda context, I feel like the routing should be handled by API Gateway itself, then forwarding the request to specific lambda functions for each resource or endoint.
- The other reason is just fun.

*N.B: I find it useful to declare the API Gateway -> Lambda routing using the amazing [serverless](https://www.serverless.com/) framework*

## Next steps:

- Implement response validation
- Add tests
