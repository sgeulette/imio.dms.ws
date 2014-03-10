# -*- coding: utf-8 -*-

from plone.jsonapi.core.browser import router


@router.add_route("/test", "test", methods=["GET"])
def test(context, request):
    return {
        "url": router.url_for("test", force_external=True),
    }
