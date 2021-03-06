# -*- coding: utf-8 -*-

import os
import sys
import urllib
from z3c.json.converter import JSONWriter
from Products.CPUtils.utils import runCommand, error, verbose
#from Products.CPUtils.utils import writeTo
from imio.dms.ws.utils import encodeFile, DATA_DIR


def ws_test(http_server, port, site):
    """
        test method to call a ws route.
        Usage: bin/ws_test the_wanted_route
    """
    json_params = {
        'test': {},
        'send_dmsfile': {
            'post': {
                'barcode': '123456789',
                'type': 'FACT',
                'pages_number': 1,
                'client_id': '111',
                'scan_date': '2014-02-12',
                'scan_hour': '10:12:53',
                'user': 'jeanjean',
                'pc': 'pc321',
                'creator': 'webservice',
                'filesize': 61278,
                'filename': '123456789.pdf',
                'data': encodeFile(os.path.join(DATA_DIR, 'courrier1.pdf')),
            },
        },
        'get_schema': {
            'get': {
                'schema': 'send_dmsfile_in',
            }
        }
    }

    args = sys.argv[1:]
    if len(args) < 1:
        error("Mandatory parameter: the_route_to_test (one of %s)" % ','.join(json_params.keys()))
        return

    route = args[0]
    #(http_server, port, site) = ('webservice-ged.communesplone.be', '80', 'webservice/webservice')
    #writeTo(os.path.join(DATA_DIR, 'sent.txt'), json_params[route]['post']['data'])
    url = "http://%s:%s/%s/@@API/%s" % (http_server, port, site, route)
    user = 'webservice'
    pwd = 'serviceweb'
    cmd = "wget -q -O - --user=%s --password=%s --auth-no-challenge" % (user, pwd)
    if route in json_params:
        if 'post' in json_params[route]:
            data = "json=%s" % JSONWriter().write(json_params[route]['post']).encode('utf8')
            #writeTo(os.path.join(DATA_DIR, 'sent.txt'), data)
            cmd += " --post-data='%s'" % data
        elif 'get' in json_params[route]:
            url += '?%s' % urllib.urlencode(json_params[route]['get'])
    cmd += ' %s' % url
    (out, err) = runCommand(cmd)
    if err:
        error('\n'.join(err))
    if out and out[0] != '\n':
        verbose('\n'.join(out))
