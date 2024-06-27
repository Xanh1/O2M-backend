schema_save_sensor = {
    "type": "object",
    "properties": {
        'ip': {"type": "string"},
        'element_type': {"type": "string"},
        'person': {"type": "string"},
        'name': {"type": "string"}

    },
    "required": ['ip', 'element_type', 'person','name']
}

schema_modify_sensor = {
    "type": "object",
    "properties": {
        'ip': {"type": "string"},
        'element_type': {"type": "string"},
        'name': {"type": "string"}

    },
    "required": ['ip', 'element_type','name']
}

schema_modify_Status_sensor = {
    "type": "object",
    "properties": {
        "uid": {"type": "string"}
    },
    "required": ["uid"]
}
