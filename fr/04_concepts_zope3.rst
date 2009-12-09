=======================
Concepts de base Zope 3
=======================

Définition
==========
ZCA (Zope Component Architecture), le modèle de composants de Zope 3 est utilisé partout dans les dernières versions de Plone. L'apprentissage des concepts de Zope 3 est nécessaire pour comprendre le fonctionnement de Plone 3.

Savoir
======
- Interfaces
- Adapters
- Utilities
- MultiAdapter et vue (sera vu plus en détails avec le chapitre TAL/METAL)
- ZCML
- Approche Grok


Installation de five.grok
=========================
Modifiez votre buildout.cfg comme ceci : ::

    [zope2]
    skip-fake-eggs =
        zope.app.publisher
        zope.component
        zope.i18n
        zope.interface
        zope.testing

    [instance]
    eggs =
        ...
        five.grok

    zcml =
        ...
        five.grok-meta
        five.grok

Et ajoutez ces versions dans votre fichier versions.cfg : ::

    five.grok = 1.0
    grokcore.annotation = 1.1
    grokcore.component = 1.7
    grokcore.formlib = 1.4
    grokcore.security = 1.2
    grokcore.site = 1.1
    grokcore.view = 1.12.2
    grokcore.viewlet = 1.3
    five.localsitemanager = 1.1
    martian = 0.11
    zope.app.publisher = 3.5.1
    zope.app.zcmlfiles = 3.4.3
    zope.component = 3.5.1
    zope.i18n = 3.4.0
    zope.interface = 3.4.1
    zope.schema = 3.4.0
    zope.securitypolicy = 3.4.1
    zope.testing = 3.7.6

Vous pouvez retrouver les dernières versions des packages qui fonctionnent bien ensemble dans le buildout de `five.grok <http://svn.zope.org/repos/main/five.grok/trunk/>`_.

Créez un product formation.transforms avec le template paster plone : ::

    $ cd /tmp
    $ paster create -t plone formation.transforms --svn-repository=http://devagile/Formation/packages
    $ cd formation.transforms
    $ svn rm --force formation.transforms/formation.transforms.egg-info
    $ svn ci -m"Added skel of formation.transforms"

Dans votre buildout, éditez le fichier *sources.cfg*, ajoutez *formation.transforms* dans l'option auto-checkout et indiquez l'url suivante dans [sources] : ::

    formation.transforms = svn http://devagile/Formation/packages/formation.transforms/trunk

Dans *buildout.cfg*, ajoutez formation.transforms dans l'option *eggs*.

Relancez ``bin/buildout`` pour récupérer le product dans le dossier src.

éditez  *src/formation.transforms/setup.py* pour déclarer le produit comme plugin plone : ::

    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """

Relancez ``bin/buildout`` pour regénérer les métadonnées de formation.transforms.

Créez un fichier *formation/transforms/interfaces.py* : ::

    from zope.interface import Interface
    
    class IReplaceLetter(Interface):
        def getText(letter1, letter2):
            """Return a modified text, replace letter1 by letter2.
            """

Créez un fichier *adapters.py* : ::

    from five import grok
    from formation.transforms.interfaces import IReplaceLetter
    from Products.ATContentTypes.interface.document import IATDocument
    
    class ReplaceLetter(grok.Adapter):
        grok.implements(IReplaceLetter)
        grok.context(IATDocument)
        def getText(self, letter1, letter2):
            return self.context.getText().replace(letter1, letter2)
    
Créez un module *views.py* : ::

    from five import grok
    from formation.transforms.interfaces import IReplaceLetter
    from Products.ATContentTypes.interface.document import IATDocument

    grok.templatedir('templates')

    class TransformedDocument(grok.View):
        grok.name("my-view")
        grok.context(IATDocument)

        def update(self, letter1=None, letter2=None):
            self.letter1 = letter1
            self.letter2 = letter2

        def getAuthenticatedUser(self):
            user = self.request.AUTHENTICATED_USER
            return user.getProperty('fullname', user.getId())

        def getContent(self):
            if self.letter1 is None or self.letter2 is None:
                return self.context.getText()
            return IReplaceLetter(self.context).getText(self.letter1, self.letter2)


Créez le répertoire *templates* et créez dedans un fichier *transformeddocument.pt* : ::

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="formation.transforms">
        <div metal:fill-slot="content"
             tal:content="structure view/getContent">
        </div>
    </html>
    

Dans *formation/transforms/configure.zcml*, ajoutez le namespace grok et la ligne : ::

    <grok:grok package=".adapters" />
    <grok:grok package=".views" />

Vous pouvez également faire : ::

    <grok:grok package="." />

qui va rechercher l'ensemble des packages et modules qui comportent des classe héritant de grok.

Dans Plone, créez un Document et accédez à la vue @@transformeddocument.

Ressources
==========
Création d'une viewlet qui affiche un Avertissement lorsque le document est expiré :
http://vincentfretin.ecreall.com/articles/creating-a-viewlet-with-grok

Viewlets avec grok
------------------
- http://grok.zope.org/documentation/how-to/understanding-viewlets
- http://grok.zope.org/documentation/how-to/fred-wilma-revisited

Zope 3 et ZCA
-------------
- Article Zope Component Architecture (ZCA) dans Linux Magazine hors-série n°40
- `Web Component Development with Zope 3 <http://worldcookery.com/>`__, Third Edition, Philipp von Weitershausen
- `A Comprehensive Guide to Zope Component Architecture <http://plone.org/documentation/books/guide-to-zca>`__
- `Zope 3 Components <http://wiki.zope.org/zope3/ZopeGuideComponents>`__
- `Zope 3 Interface <http://wiki.zope.org/zope3/ZopeGuideInterfaces>`__
- `Grok Configuration Phase and its Extension <http://exploring-grok.blogspot.com/2009/01/grok-configuration-phase-and-its.html>`__
