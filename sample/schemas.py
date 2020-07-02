user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}
    },
    "required": ["name"],
    "additionalProperties": False
}

get_users_query_params_schema = {
    "type": ["object", "null"],
    "properties": {
        "page": {"type": "string"}
    },
    "additionalProperties": False
}
