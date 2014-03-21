# -*- coding: utf-8 -*-

import os
import base64
import tempfile
import imio.dms.ws as idw
#from Products.CPUtils.utils import verbose

DATA_DIR = os.path.join(idw.__path__[0], 'data')


def encodeFile(filepath):
    """
        Encode a file in a base64 string
    """
    try:
        if os.path.exists(filepath):
            ofile = open(filepath, 'rb')
            data = ofile.read()
            ofile.close()
            return base64.urlsafe_b64encode(data)
        else:
            return "File %s doesn't exist" % filepath
    except IOError:
        return "Cannot open %s file" % filepath

#------------------------------------------------------------------------------


def decodeToFile(b64str, temp=True, filepath='', close=False):
    """
        Decode a base64 string to file.
        If temp = True, create a temporary file and return a file object.
        If temp = False, create a file at the given filepath and return the size.
    """
    try:
        if temp:
            ofile = tempfile.NamedTemporaryFile()
        elif filepath:
            ofile = open(filepath, 'wb')
        ofile.write(base64.urlsafe_b64decode(b64str))
        size = ofile.tell()
        if close:
            ofile.close()
        return (ofile, size)
    except IOError:
        return "Cannot create %s file" % filepath
