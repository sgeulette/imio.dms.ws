# -*- coding: utf-8 -*-

from zope.component import getUtility
from z3c.json.interfaces import IJSONWriter
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
            "creator": {
                "description": "The plone login name used for object creation",
                "type": "string",
                "minLength": 1,
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
        "required": ["barcode", "type", "client_id", "scan_date", "scan_hour", "creator", "filesize",
                     "filename", "data"]
    },
    'send_dmsfile_out': {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "Json validation schema for output document",
        "description": "This schema is used to validate json data sent when proposing "
                       "a document to the imio webservice.",
        "type": "object",
        "properties": {
            "success": {
                "description": "Status flag",
                "type": "boolean",
            },
            "message": {
                "description": "Status message",
                "type": "string",
            },
            "barcode": {
                "description": "The unique identifier of a document",
                "type": "string",
            },
            "input": {
                "description": "Input json. Only when validation problem",
                "type": "string",
            },
            "_runtime": {
                "description": "Server process duration",
                "type": "string",
            },
            "error": {
                "description": "Error message with traceback. Only when uncatched error",
                "type": "string",
            },
        },
        "required": ["success", "message", ]
    },
}


@router.add_route("/get_schema", "get_schema", methods=["GET"])
def get_schema(context, request):
    """
        Webservice method to get a schema
    """
    schema = request.get('schema', '')
    if not schema:
        return helpers.error('You must give a schema name as parameter: /get_schema?schema=xxx.'
                             'The following schema names are available: %s' % ", ".join(all_schemas.keys()))
    if not schema in all_schemas:
        return helpers.error("The asked schema '%s' doesn't exist" % schema)
    jsonWriter = getUtility(IJSONWriter)
    return helpers.success("Got schema %s" % schema, schema=jsonWriter.write(all_schemas[schema]))
