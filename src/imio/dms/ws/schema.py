# -*- coding: utf-8 -*-

from plone.jsonapi.core.browser import router, helpers

all_schemas = {
    'send_dmsfile_in': {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "Json validation schema for input document",
        "description": "This schema is used to validate json data sent when proposing "
                       "a document to the imio webservice.",
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
    },
}


@router.add_route("/get_schema/<string:schema>", "get_schema", methods=["GET"])
def get_schema(context, request, schema=''):
    """
        Webservice method to get a schema
    """
    if not schema:
        return helpers.error('You must give a schema name as parameter: /get_schema/the-schema-name.'
                             'The following schema names are available: %s' % all_schemas.keys())
#    jsonReader = getUtility(interfaces.IJSONReader)
