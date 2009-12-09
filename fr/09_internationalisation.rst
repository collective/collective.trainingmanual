===================================
Internationalisation d'un composant
===================================

Plone est multilingue. Cette partie explique comment rendre votre composant disponible en plusieurs langues. 

Savoir
======
- i18n dans du code Python
- i18n dans les page templates
- extraction des chaines avec i18ndude 

Créez un environnement avec i18ndude d'installé : ::

    $ mkvirtualenv i18n
    $ easy_install i18ndude

Dans *Products/AgileKnowledgeBase* créez un script *update-l10n.sh* : ::

    i18ndude rebuild-pot --pot i18n/kb-plone.pot --create plone profiles
    i18ndude filter i18n/kb-plone.pot ~/.buildout/eggs/plone.app.locales-3.3.1-py2.4.egg/plone/app/locales/i18n/plone.pot > i18n/kb-plone.pot_
    mv i18n/kb-plone.pot_ i18n/kb-plone.pot
    i18ndude sync --pot i18n/kb-plone.pot i18n/kb-plone-*.po

    i18ndude rebuild-pot --pot locales/AgileKnowledgeBase.pot --create AgileKnowledgeBase .
    i18ndude sync --pot locales/AgileKnowledgeBase.pot locales/*/LC_MESSAGES/AgileKnowledgeBase.po

Exécutez ``i18ndude -h`` pour savoir à quoi servent les différentes commandes.

Installez le package Ubuntu *gettext* qui contient notamment la commande *msginit*. Installez également poedit (ou kbabel) pour traduire facilement : ::

    $ sudo apt-get install gettext poedit

Exécutez le script *update-l10n.sh*, pour cela ajoutez le mode exécution : ::

    $ chmod u+x update-l10n.sh
    $ ./update-l10n.sh

La première exécution du script échouera pour les commandes ``i18ndude sync`` car il n'y a encore aucune traduction.

Vous allez donc maintenant initialiser la traduction française : ::

    $ msginit -i i18n/kb-plone.pot -o i18n/kb-plone-fr.po

La commande *msginit* fait une copie du fichier pot en fichier po et remplie certains headers comme la date et le traducteur.

Ouvrez ensuite kb-plone-fr.po pour finir de remplir les headers.
Remplacez notamment PACKAGE par AgileKnowledgeBase, supprimez VERSION et surtout modifiez ces headers : ::

    "Language-Code: fr\n"
    "Language-Name: French\n"

Vous pouvez maintenant passer à la traduction : ::

    $ poedit i18n/kb-plone-fr.po

Vous utiliserez le dossier i18n uniquement pour le domaine *plone*.


Pour le domaine de votre produit, vous utiliserez le nouveau dossier *locales* qui est le standard gettext.

Pour le domaine *AgileKnowledgeBase*, il vous faut tout d'abord créer le dossier : ::

    $ mkdir -p locales/fr/LC_MESSAGES

Générez le fichier AgileKnowledgeBase.pot avec le script : ::

    $ ./update-l10n.sh

Ensuite créez le fichier de traduction : ::

    $ msginit -i locales/AgileKnowledgeBase.pot -o locales/fr/LC_MESSAGES/AgileKnowledgeBase.po

éditez les headers du fichier po comme ceci : ::

    "Language-Code: fr\n"
    "Language-Name: French\n"
    "Domain: AgileKnowledgeBase\n"

Traduisez ensuite avec poedit.

Pour que vos traductions soient prises au démarrage de l'instance, vous devez également avoir la directive *i18n:registerTranslations* dans votre *configure.zcml*, par exemple : ::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:grok="http://namespaces.zope.org/grok"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        i18n_domain="formation.transforms">

        <i18n:registerTranslations directory="locales" />

        <grok:grok package="." />

    </configure>


Ressources
==========
- http://plone.org/documentation/how-to/product-skin-localization
- http://plone.org/documentation/how-to/i18n-for-developers
- http://www.mattdorn.com/content/plone-i18n-a-brief-tutorial/
- http://grok.zope.org/documentation/how-to/how-to-internationalize-your-application
- http://maurits.vanrees.org/weblog/archive/2007/09/i18n-locales-and-plone-3.0
- http://dev.plone.org/plone/wiki/TranslationGuidelines
- http://n2.nabble.com/Recipe-for-overriding-translations-td3045492ef221724.html

Voir http://dev.plone.org/plone/ticket/9090 pour l'état de la fusion des documents ci-dessus.

Exercice
========
Traduction du template de mail créé précédemment.
