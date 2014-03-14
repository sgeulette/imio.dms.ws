# -*- coding: utf-8 -*-
"""Init and utils."""
import zope.component

from zope.i18nmessageid import MessageFactory
from z3c.json.interfaces import IJSONReader, IJSONWriter
from z3c.json import converter

_ = MessageFactory('imio.dms.ws')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    zope.component.provideUtility(converter.JSONReader(), IJSONReader)
    zope.component.provideUtility(converter.JSONWriter(), IJSONWriter)
