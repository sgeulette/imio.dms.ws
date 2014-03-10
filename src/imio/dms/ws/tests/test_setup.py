# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from imio.dms.ws.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of imio.dms.ws into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if imio.dms.ws is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('imio.dms.ws'))

    def test_uninstall(self):
        """Test if imio.dms.ws is cleanly uninstalled."""
        self.installer.uninstallProducts(['imio.dms.ws'])
        self.assertFalse(self.installer.isProductInstalled('imio.dms.ws'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IImioDmsWsLayer is registered."""
        from imio.dms.ws.interfaces import IImioDmsWsLayer
        from plone.browserlayer import utils
        self.assertIn(IImioDmsWsLayer, utils.registered_layers())
