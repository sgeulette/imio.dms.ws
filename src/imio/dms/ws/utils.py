# -*- coding: utf-8 -*-

import os
import base64


def convertBinary(filepath):
    """
        Read the file argument and prepare it to json
    """
    try:
        if os.path.exists(filepath):
            ofile = open(filepath, 'rb')
            data = ofile.read()
            ofile.close()
            return base64.b64encode(data)
        else:
            return "File %s doesn't exist" % filepath
    except IOError:
        return "Cannot open %s file" % filepath


#------------------------------------------------------------------------------
