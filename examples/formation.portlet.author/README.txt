.. $Id$

=============
AuthorPortlet
=============

Attach this portlet to a content type. It shows the author portrait
and a link to its personal page.

Requirements
============

Plone 3, Plone 4 on any platform.

Installation
============

Zope instance
-------------

Edit your buildout configuration::

  [instance]
  recipe = plone.recipe.zope2instance
  ...
  eggs =
      ...
      formation.portlet.author
      ...

Plone site
----------

Add with the quickinstaller or using GenericSetup or using the Modules Plone
control panel as usual to have this portlet available in your site.

Visit any portlet manager (folder, types, or groups), add the portlet and
configure it the way you prefer.

Copyright and license
=====================

This software is subject to the provisions of the GNU General Public License,
Version 2.0 (GPL).  A copy of the GPL should accompany this distribution.  THIS
SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE
DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE,
MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE

See the `LICENSE` file that comes with this product.

Support and feedback
--------------------

This is an unsupported demo component. Should you have any question about it,
help yourself...
