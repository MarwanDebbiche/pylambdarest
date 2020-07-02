from pylambdarest import route
from schemas import (
    user_schema,
    get_users_query_params_schema
)


@route()
def hello():
    return 200, {"messsage": "Hello from pylambdarest !!!"}


@route()
def get_user(request):
    user_id = request.path_params.get("user_id")

    # request db data for user <user_id> here
    user = {
        "userId": user_id,
        "name": "John Doe"
    }

    return 200, user


@route(body_schema=user_schema, )
def create_user(request, event):

    # Create user here

    return 201


@route(query_params_schema=get_users_query_params_schema)
def get_users(request, event):
    page = int(request.query_params.get("page", 1))

    # request users in db
    users = [
        {"userId": i}
        for i in range((page - 1) * 50, page * 50)
        # for i in range(10)
    ]

    return 200, users
