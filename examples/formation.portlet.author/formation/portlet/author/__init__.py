# -*- coding: utf-8 -*-
# $Id$
"""The formation.portlet.author package"""

import logging
from zope.i18nmessageid import MessageFactory
import config

# We use this object for logging anything
logger = logging.getLogger(config.PRODUCTNAME)

# Localizing messages from Python
AuthorPortletMessageFactory = MessageFactory(config.I18N_DOMAIN)
