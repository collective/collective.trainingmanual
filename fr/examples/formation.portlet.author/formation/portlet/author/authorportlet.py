# -*- coding: utf-8 -*-
# $Id$
"""The portlet definition, the main module of our component"""
from zope.interface import implements
from zope.component import getMultiAdapter
from zope import schema
from zope.formlib import form
from Acquisition import aq_inner
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from formation.portlet.author import AuthorPortletMessageFactory as _
from formation.portlet.author import logger

# Set logging in debug mode using buildout.cfg using "event-log-custom" option.
LOG = logger.debug

class IAuthorPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    show_details = schema.Bool(
        title=_(u'Show author details'),
        description=_(u'When checked, the portlet show the biography and the home page link'),
        default=False
        )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IAuthorPortlet)

    # TODO: Set default values for the configurable parameters here
    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self, show_details=False):
        """Configurable parameter are provided as keyword arguments
        Use the same names as in the schemaof IAuthorPortlet
        """
        self.show_details = show_details
        return

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u'Author')



class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    _template = ViewPageTemplateFile('authorportlet.pt')

    def __init__(self, *args):
        """We prepare the various attributes for the view
        """
        super(Renderer, self).__init__(*args)
        context = aq_inner(self.context)
        # (Suposed to be) faster than "old fashioned" getToolByName
        plone_tools = getMultiAdapter((self.context, self.request), name=u"plone_tools")

        author_id = context.Creator()
        LOG("Author '%s' found", author_id)
        self.portal_membership = plone_tools.membership()
        author_member = self.portal_membership.getMemberById(author_id)
        if author_member:
            # Okay, we got a valid author member
            LOG("Author obj %s exists", str(author_member))
            member_prop = author_member.getProperty
            self.author_id = author_id
            self.visible_member = bool(member_prop('listed'))
            LOG("visible_member %s" % self.visible_member)
            self.author_name = member_prop('fullname')
            self.location = member_prop('location')
            self.description = member_prop('description')
            self.home_page = member_prop('home_page')
        else:
            self.author_id = None
            self.visible_member = False
        return

    @property
    def available(self):
        """Should we show this portlet
        This attrib is checked to show or not the portlet
        This attribute MUST be provided from any portlet
        """
        return self.visible_member

    def render(self):
        """Provides the HTML of the portlet
        This method MUST be provided from any portlet
        """
        LOG("Rendering the author portlet")
        return xhtml_compress(self._template())

    # The following methods are available from authorportlet.pt from the
    # 'view' variable. e.g tal:content="view/member_page"


    def portrait_url(self):
        """URL to the portrait image or None"""

        portrait = self.portal_membership.getPersonalPortrait(self.author_id)
        if portrait:
            return portrait.absolute_url()
        return None


    def show_details(self):
        """Shortcut to portlet props"""

        return self.data.show_details


    def member_page(self):
        """Link to author resume page"""

        plone_tools = getMultiAdapter((self.context, self.request), name='plone_tools')
        portal_url = plone_tools.url()
        return '%s/author/%s' % (portal_url(), self.author_id)


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IAuthorPortlet)
    label = _(u'Add Author Portlet')
    description = _(u'This portlet shows details on the author of published content')

    def create(self, data):
        return Assignment(show_details=data.get('show_details', False))


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IAuthorPortlet)
    label = _(u'Edit Author Portlet')
    description = _(u'This portlet shows details on the author of published content')

