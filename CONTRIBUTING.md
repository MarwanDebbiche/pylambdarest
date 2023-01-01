# How to contribute to restful-aws-lambda

Thank you for considering contributing to restful-aws-lambda!

## First time setup

- Make sure you have a [GitHub account](https://github.com/join).

- Fork restful-aws-lambda to your GitHub account by clicking the [Fork](https://github.com/joffreybvn/restful-aws-lambda/fork) button.

- Install [poetry](https://python-poetry.org/).

- Install dependecies using poetry:

```shell
poetry install
```

- Install the pre-commit hooks:

```shell
poetry run pre-commit install --install-hooks
```

- Run the tests to make sure you are all set:

```shell
poetry run coverage run -m --source=restful_aws_lambda pytest tests && poetry run coverage report -m
```

## Building the docs

Build the docs in the docs directory using Sphinx:

```shell
cd docs
poetry run make html
```

Open `build/html/index.html` in your browser to view the docs.

Read more about [Sphinx](https://www.sphinx-doc.org/en/master/).

## Submitting patches

Include the following in your patch:

- Use Black to format your code. This and other tools will run automatically if you install pre-commit using the instructions above.
- Include tests if your patch adds or changes code. Make sure the test fails without your patch.
- Update the documentation accordingly if needed.
