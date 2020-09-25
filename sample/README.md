# Sample project

This sample project demonstrates how you can use pylambdarest with [serverless](https://serverless.com/) to build and deploy your own REST API.

The [serverless.yaml](./serverless.yaml) defines the API Gateway routing.

Handlers are defined in [handler.py](./handler.py) using pylambdarest.

# Install dependencies

**With [Poetry](https://python-poetry.org/):**
```
poetry install
```

**With pip:**
```
pip install -r requirements.txt
```

*N.B: If you use pip instead of poetry for dependency management, you will need to change `usePoetry: true` to `usePoetry: false` in the serverless.yaml.*

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
