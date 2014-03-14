# -*- coding: utf-8 -*-

import os
from zope.component import getUtility
from z3c.json.interfaces import IJSONReader
from plone.jsonapi.core.browser import router, helpers
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
#from Products.CPUtils.utils import writeTo
#from Products.CPUtils.utils import error
from jsonschema import validate, ValidationError
from imio.dms.ws.utils import decodeToFile, DATA_DIR
from imio.dms.ws.schema import all_schemas


@router.add_route("/test", "test", methods=["GET"])
def test(context, request):
    return {
        "url": router.url_for("test", force_external=True),
    }


@router.add_route("/send_dmsfile", "send_dmsfile", methods=["POST"])
def send_dmsfile(context, request):
    """
        Webservice method to send a dms file and create a plone object
    """
#    if not getSecurityManager().checkPermission("Manage portal", context):
#        raise Unauthorized("You cannot access this webservice")

    jsonReader = getUtility(IJSONReader)
    json_data = request.get('json', '')
    if not json_data:
        return helpers.error("Missing json parameter in the post data of the request")
    input_params = jsonReader.read(json_data)
    try:
        validate(input_params, all_schemas['send_dmsfile_in'])
    except ValidationError, ve_obj:
        del input_params['data']
        msg = 'Validation error'
        if len(ve_obj.path):
            msg += " on '%s'" % ', '.join(ve_obj.path)
        return helpers.error("%s: %s" % (msg, ve_obj.message),
                             barcode=input_params['barcode'],
                             input=input_params)

    # needed to be encoded for base64 translation
    input_params['data'] = input_params['data'].encode('utf8')
#    writeTo(os.path.join(DATA_DIR, 'received.txt'), input_params['data'])
    size = decodeToFile(input_params['data'], os.path.join(DATA_DIR, input_params['filename']))
    input_params['data'] = "data length %d" % size

    if input_params['filesize'] != size:
        return helpers.error("The decoded file content has not the original size: %d <> %d"
                             % (size, input_params['filesize']), input=input_params, barcode=input_params['barcode'])

    return helpers.success("Well done", input=input_params, barcode=input_params['barcode'])
