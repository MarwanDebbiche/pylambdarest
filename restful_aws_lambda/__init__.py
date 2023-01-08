"""
restful_aws_lambda - RESTful API with AWS Lambda and API Gateway.
"""

from restful_aws_lambda.decorator import route
from restful_aws_lambda.request import Request

__all__ = ["route", "Request"]
