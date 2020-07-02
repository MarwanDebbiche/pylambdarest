from pylambdarest import route
from schemas import user_schema


@route()
def hello():
    return 200, {"messsage": "Hello from pylambdarest !!!"}


@route()
def get_user(request, event):
    user_id = request.path_params.get("user_id")

    user = {}  # Fetch data for user <user_id> here

    return 200, user


@route(body_schema=user_schema)
def create_user(request, event):

    # Create user here

    return 201, {}
