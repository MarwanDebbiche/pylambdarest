auth_schema = {
    "type": "object",
    "properties": {"username": {"type": "string"}, "password": {"type": "string"}},
    "required": ["username", "password"],
    "additionalProperties": False,
}


get_users_query_params_schema = {
    "type": ["object", "null"],
    "properties": {"page": {"type": "string"}},
    "additionalProperties": False,
}
