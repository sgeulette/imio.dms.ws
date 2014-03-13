# -*- coding: utf-8 -*-

input_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Json validation schema for input document",
    "description": "This schema is used to validate json data sent when proposing a document to the imio webservice.",
    "type": "object",
    "properties": {
        "barcode": {
            "description": "The unique identifier of a document",
            "type": "string"
        }
    },
    "required": ["barcode"]

}
