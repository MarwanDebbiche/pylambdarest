# Sample project

This sample project demonstrates how you can use pylambdarest with [serverless](https://serverless.com/) to build and deploy your own REST API.

The [serverless.yaml](./serverless.yaml) defines the API Gateway routing.

You can deploy the API using serverless:

```
serverless deploy --stage development
```

And you can test the API locally using [serverless-offline](https://github.com/dherault/serverless-offline):

```
serverless offline
```
