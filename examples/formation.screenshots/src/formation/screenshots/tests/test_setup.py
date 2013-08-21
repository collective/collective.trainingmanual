# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from formation.screenshots.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of formation.screenshots into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if formation.screenshots is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('formation.screenshots'))

    def test_uninstall(self):
        """Test if formation.screenshots is cleanly uninstalled."""
        self.installer.uninstallProducts(['formation.screenshots'])
        self.assertFalse(self.installer.isProductInstalled('formation.screenshots'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IFormationScreenshotsLayer is registered."""
        from formation.screenshots.interfaces import IFormationScreenshotsLayer
        from plone.browserlayer import utils
        self.failUnless(IFormationScreenshotsLayer in utils.registered_layers())
