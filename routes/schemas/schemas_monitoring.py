schema_save = {
    "type": "object",
    "properties": {
        "start_date": {"type": "string", "format": "date-time"},
        "end_date": {"type": "string", "format": "date-time"},
        "data": {"type": "number"},
        "uid": {"type": "string"}
    },
    "required": ["start_date", "end_date", "data", "uid"]
}
