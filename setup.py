import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylambdarest",
    version="0.0.4",
    author="Marwan Debbiche",
    author_email="marwan.debbiche@gmail.com",
    description="REST framework for serverless API (AWS Lambda + API Gateway)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarwanDebbiche/pylambdarest",
    packages=['pylambdarest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['jsonschema']
)
