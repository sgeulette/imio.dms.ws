# -*- coding: utf-8 -*-

import os
from zope.component import getUtility
from z3c.json import interfaces
from plone.jsonapi.core.browser import router
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
#from Products.CPUtils.utils import writeTo
from imio.dms.ws.utils import decodeToFile, DATA_DIR


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

    jsonReader = getUtility(interfaces.IJSONReader)
    input_params = jsonReader.read(request.get('json', ''))
    input_params['data'] = input_params['data'].encode('utf8')
#    writeTo(os.path.join(DATA_DIR, 'received.txt'), input_params['data'])
    decodeToFile(input_params['data'], os.path.join(DATA_DIR, 'courrier1_recup.pdf'))
    input_params['data'] = "b64 data length %d" % len(input_params['data'])
    return {
        'input': input_params
    }
