# -*- coding: utf-8 -*-

import os
import sys
from z3c.json.converter import JSONWriter
from Products.CPUtils.utils import runCommand, error, verbose
from imio.dms.ws.utils import convertBinary
import imio.dms.ws as idw


def ws_test(http_server, port, site):
    """
        test method to call a ws route.
        Usage: bin/ws_test the_wanted_route
    """
    args = sys.argv[1:]
    if len(args) < 1:
        error("Mandatory parameter: the_route_to_test (send_dmsfile or test)")
        return

    json_params = {
        'test': {},
        'send_dmsfile': {
            'post': {
                'barcode': 'IMIO123456789',
                'type': 'FACT',
                'pages_number': 2,
                'client_id': '111',
                'scan_date': '12022014',
                'scan_hour': '10:12:53',
                'user': 'jeanjean',
                'pc': 'pc321',
                'data': convertBinary(os.path.join(idw.__path__[0], 'data', 'courrier1.pdf')),
            },
        }
    }
    route = args[0]
    url = "http://%s:%s/%s/@@API/%s" % (http_server, port, site, route)
    user = pwd = 'admin'
    cmd = "wget -q -O - --user=%s --password=%s" % (user, pwd)
    if route in json_params:
        if 'post' in json_params[route]:
            #data = urllib.urlencode(json_params[route]['post'])
            data = "json=%s" % JSONWriter().write(json_params[route]['post']).encode('utf8')
            cmd += " --post-data='%s'" % data
    cmd += ' %s' % url
    (out, err) = runCommand(cmd)
    if err:
        error('\n'.join(err))
    if out and out[0] != '\n':
        verbose('\n'.join(out))
