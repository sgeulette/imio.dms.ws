# -*- coding: utf-8 -*-

import datetime
import os
from zope.component import getUtility
from z3c.json.interfaces import IJSONReader
from plone.jsonapi.core.browser import router, helpers
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from plone import api
from plone.namedfile.file import NamedBlobFile
#from Products.CPUtils.utils import writeTo
#from Products.CPUtils.utils import error
from collective.dms.batchimport.utils import createDocument
from jsonschema import validate, ValidationError
from imio.dms.ws.utils import decodeToFile, DATA_DIR
from imio.dms.ws.schema import all_schemas

portal_types = {
    'COUR_E': {
        'pt': 'dmsincomingmail',
        'folder': 'incoming-mail',
    },
    'COUR_S': {
        'pt': 'dmsoutgoingmail',
        'folder': 'outgoing-mail',
    },
    'FACT': {
        'pt': 'dmsincomingmail',
        'folder': 'incoming-mail',
    },
}


@router.add_route("/send_dmsfile", "send_dmsfile", methods=["POST"])
def send_dmsfile(context, request):
    """
        Webservice method to send a dms file and create a plone object
    """
    if not getSecurityManager().checkPermission("imio.dms.ws: Use webservice", context):
        raise Unauthorized("You cannot access this webservice")

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
    # check fields content
    # scan_date: YYYY-MM-DD
    try:
        scan_date = datetime.date(int(input_params['scan_date'][0:4]), int(input_params['scan_date'][5:7]),
                                  int(input_params['scan_date'][8:10]))
    except Exception, value_error:
        return helpers.error("Uncorrect scan_date value ('%s'): %s" % (input_params['scan_date'], value_error),
                             barcode=input_params['barcode'])
    # scan_hour: HH:mm:SS
    try:
        scan_time = datetime.time(int(input_params['scan_hour'][0:2]), int(input_params['scan_hour'][3:5]),
                                  int(input_params['scan_hour'][6:8]))
    except Exception, value_error:
        return helpers.error("Uncorrect scan_hour value ('%s'): %s" % (input_params['scan_hour'], value_error),
                             barcode=input_params['barcode'])
    # creator
    if api.user.get(username=input_params['creator']) is None:
        return helpers.error("The creator '%s' doesn't exist" % input_params['creator'],
                             barcode=input_params['barcode'])

    # needed to be encoded for base64 translation
    input_params['data'] = input_params['data'].encode('utf8')
#    writeTo(os.path.join(DATA_DIR, 'received.txt'), input_params['data'])

    portal = api.portal.get()
    # check cross links
    if input_params['type'] not in portal_types:
        return helpers.error("This document type '%s' isn't configured" % input_params['type'],
                             barcode=input_params['barcode'])
    if portal_types[input_params['type']]['pt'] not in portal.portal_types.listContentTypes():
        return helpers.error("The configured portal type '%s' doesn't exist in Plone" %
                             portal_types[input_params['type']]['pt'], barcode=input_params['barcode'])
    try:
        folder = portal.unrestrictedTraverse(portal_types[input_params['type']]['folder'])
    except KeyError:
        return helpers.error("The configured folder '%s' doesn't exist in Plone" %
                             portal_types[input_params['type']]['folder'],
                             barcode=input_params['barcode'])

    (fo, size) = decodeToFile(input_params['data'], filepath=os.path.join(DATA_DIR, input_params['filename']))

    if input_params['filesize'] != size:
        return helpers.error("The decoded file content has not the original size: %d <> %d"
                             % (size, input_params['filesize']), barcode=input_params['barcode'])

    # preparing data to create object

    class dummy(object):
        def __init__(self, context, request):
            self.context = context
            self.request = request

    fo.seek(0)
    metadata = {
        'id': input_params['barcode'],
        'file_title': input_params['filename'],
        'reception_date': datetime.datetime.combine(scan_date, scan_time),
#        'internal_reference_no': '',
    }
    document_file = NamedBlobFile(fo.read(), filename=input_params['filename'])
    createDocument(dummy(context, request), folder, portal_types[input_params['type']]['pt'], '',
                   document_file, owner=input_params['creator'], metadata=metadata)
    fo.close()

    return helpers.success("Well done", barcode=input_params['barcode'])
