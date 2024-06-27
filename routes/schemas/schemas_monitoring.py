schema_save = {
    "type": "object",
    "properties": {
        "latitude": {"type": "string"},
        "longitude": {"type": "string"},
        "start_date": {"type": "string", "format": "date-time"},
        "end_date": {"type": "string", "format": "date-time"},
        "data": {"type": "number"},
        "uid": {"type": "string"}
    },
    "required": ["latitude", "longitude", "start_date", "end_date", "data", "uid"]
}
