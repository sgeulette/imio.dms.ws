# -*- coding: utf-8 -*-

from plone import api


def isNotCurrentProfile(context):
    return context.readDataFile("imiodmsws_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return
    portal = context.getSite()
    # create a test user
    api.user.create(email="test@test.be", username="webservice", password="serviceweb", roles=('Member'))
