# Sample project

This sample project demonstrates how you can use pylambdarest with [serverless](https://serverless.com/) to build and deploy your own REST API.

The [serverless.yaml](./serverless.yaml) defines the API Gateway routing.

Handlers are defined in [handler.py](./handler.py) using pylambdarest.

# Install js dependencies

You need to have [Node.js](https://nodejs.org/en/) installed to run this sample project.
You can then use npm to install dependencides:

```
npm install
```

# Install python dependencies

**With [Poetry](https://python-poetry.org/):**

```
poetry install
```

**With pip:**

```
pip install -r requirements.txt
```

_N.B: If you use pip instead of poetry for dependency management, you will need to change `usePoetry: true` to `usePoetry: false` in the serverless.yaml._

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
