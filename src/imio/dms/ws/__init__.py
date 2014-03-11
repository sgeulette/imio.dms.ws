# -*- coding: utf-8 -*-
"""Init and utils."""
import zope.component

from zope.i18nmessageid import MessageFactory
from z3c.json import interfaces
from z3c.json import converter

_ = MessageFactory('imio.dms.ws')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    zope.component.provideUtility(converter.JSONReader(), interfaces.IJSONReader)
