# -*- coding: utf-8 -*-

input_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Json validation schema for input document",
    "description": "This schema is used to validate json data sent when proposing a document to the imio webservice.",
    "type": "object",
    "properties": {
        "barcode": {
            "description": "The unique identifier of a document",
            "type": "string",
        },
        "type": {
            "description": "The type of the document",
            "type": "string",
        },
        "pages_number": {
            "description": "The number of pages",
            "type": "integer",
        },
        "client_id": {
            "description": "The id of the client",
            "type": "string",
        },
        "scan_date": {
            "description": "The scan date with format DDMMYYYY",
            "type": "string",
        },
        "scan_hour": {
            "description": "The scan hour with format HH:mm:SS",
            "type": "string",
        },
        "user": {
            "description": "The scanner post login name",
            "type": "string",
        },
        "pc": {
            "description": "The scanner post computer",
            "type": "string",
        },
        "filesize": {
            "description": "The scan file size in bytes",
            "type": "integer",
            "minimum": 0,
            "exclusiveMinimum": True,
        },
        "data": {
            "description": "The file content encoded in base64. '+' and '/' characters have to be "
                           "literally replaced by '-' and '_' characters",
            "type": "string",
        },
    },
    "additionalProperties": False,
    "required": ["barcode", "type", "client_id", "scan_date", "scan_hour", "filesize", "data"]
}
