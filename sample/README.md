# Sample project

This sample project demonstrates how you can use pylambdarest with [serverless](https://serverless.com/) to build and deploy your own REST API.

The [serverless.yaml](./serverless.yaml) defines the API Gateway routing.

Handlers are defined in [handler.py](./handler.py) using pylambdarest.

# Install dependencies

**With [Poetry](https://python-poetry.org/):**
```
poetry install
```

*N.B: For now I am unable to deploy the service using poetry due to an error with jsonschema installation. I have opened an [issue](https://github.com/UnitedIncome/serverless-python-requirements/issues/555) on the serverless-python-requirements repository*

**With pip:**
```
pip install -r requirements.txt
```

# Test

You can test the API locally using [serverless-offline](https://github.com/dherault/serverless-offline):

```
serverless offline
```

# Deploy

Deploying the API is as simple as:

```
serverless deploy
```
