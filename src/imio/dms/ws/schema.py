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
            "pattern": "^.+$",
        },
        "type": {
            "description": "The type of the document",
            "type": "string",
            "minLength": 1,
        },
        "pages_number": {
            "description": "The number of pages",
            "type": "integer",
            "minimum": 1,
        },
        "client_id": {
            "description": "The id of the client",
            "type": "string",
            "minLength": 1,
        },
        "scan_date": {
            "description": "The scan date with format YYYY-MM-DD",
            "type": "string",
            "pattern": "^\d{4}-\d{2}-\d{2}$",
#            "format": "date",
        },
        "scan_hour": {
            "description": "The scan hour with format HH:mm:SS",
            "type": "string",
            "pattern": "^\d{2}:\d{2}:\d{2}$",
#            "format": "hour",
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
        "filename": {
            "description": "The scan file name",
            "type": "string",
            "minLength": 1,
        },
        "data": {
            "description": "The file content encoded in base64. '+' and '/' characters have to be "
                           "literally replaced by '-' and '_' characters",
            "type": "string",
            "minLength": 1,
        },
    },
    "additionalProperties": False,
    "required": ["barcode", "type", "client_id", "scan_date", "scan_hour", "filesize", "filename", "data"]
}
