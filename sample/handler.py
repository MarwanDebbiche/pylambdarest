from schemas import get_users_query_params_schema, user_schema, auth_schema


from datetime import timezone, timedelta, datetime
from pylambdarest import App, Request
import jwt

config = {"AUTH_SCHEME": "JWT_BEARER", "JWT_SECRET": "secret"}


app = App(config=config)


@app.route()
def hello():
    return 200, {"message": "Hello from pylambdarest !!!"}


@app.route(body_schema=auth_schema)
def auth(request: Request):
    username = request.json["password"]
    password = request.json["username"]

    # compare password and hash (stored in db) here

    token = jwt.encode(
        {
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=30),
            "username": username,
        },
        config["JWT_SECRET"],
    )

    return 200, {"token": token}


@app.route(restricted=True)
def get_user(user_id, jwt_payload):
    print(jwt_payload)
    # request db data for user <user_id> here
    user = {"userId": user_id, "name": "John Doe"}

    return 200, user


@app.route(restricted=True, query_params_schema=get_users_query_params_schema)
def get_users(request):
    page = int(request.query_params.get("page", 1))

    # request users in db
    users = [
        {"userId": i}
        for i in range((page - 1) * 50, page * 50)
        # for i in range(10)
    ]

    return 200, users
