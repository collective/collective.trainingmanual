==============================================================
Formation de TAL/Metal permettant l'écriture de page dynamique
==============================================================

Les Zope Page Templates sont un mécanisme permettant d'écrire des pages xhtml dynamiques.
Ces ZPT utilise un langage de template XML TAL/METAL.
L'objectif est d'être capable de comprendre, créer et modifier les pages dynamiques.

Le langage TAL
==============
Savoir
------
- Liste des commandes
- Ordre d'évaluation
- Content et Replace
- Condition
- Define
- Repeat
- On-error
- Omit-tag

TALES
=====
Savoir
------
- Exemples
- Path
- Path alternatif et nothing
- Not
- String
- Nocall
- Python

METAL
=====
Savoir
------
- metal:define-macro
- metal:define-slot
- metal:use-macro
- metal:fill-slot

Ressources
==========
Lire la documentation `ZPT - Zope Page Templates`_ sur plone.org.

À noter que certains exemples avec *tal:repeat* sont faux.
Un *tal:repeat* sur une balise *ul* ou *tbody* répètera la balise à chaque tour de boucle. Le *tal:repeat* devrait donc se situer sur un *li* ou un *tr*.

Petit rappel sur les tableaux : vous pouvez mettre un *tr* dans un *thead* pour avoir une ligne d'en-tête sur chaque page lors de l'impression d'un tableau. Il va de même pour un pied de page avec la balise *tfoot*.

Dans le document ci-dessus, il manque les commandes *tal:omit-tag* et *tal:on-error*, cela est expliqué dans les ZopeBook :

- `Using Zope Page Templates`_
- `Advanced Page Templates`_
- `Appendix C: Zope Page Templates Reference`_

La documentation sur plone.org et celle dans le ZopeBook se ressemble beaucoup.
Les pages dans le ZopeBook sont complémentaires à la documentation sur plone.org.

.. _`ZPT - Zope Page Templates`: http://plone.org/documentation/tutorial/zpt
.. _`Using Zope Page Templates`: http://docs.zope.org/zope2/zope2book/source/ZPT.html
.. _`Advanced Page Templates`: http://docs.zope.org/zope2/zope2book/source/AdvZPT.html
.. _`Appendix C: Zope Page Templates Reference`: http://docs.zope.org/zope2/zope2book/source/AppendixC.html

Namespaces
==========
Prenez l'habitude de toujours inclure les namespaces dans vos templates.
Ils seront nécessaires pour le nouveau moteur de template Chameleon qui parse la page de manière stricte.

La structure minimale est donc : ::

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          xml:lang="en" lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="mydomain">
    </div>

Vous pouvez vérifier si vos templates sont bien valides XML avec la commande ``xmllint matemplate.pt``.


Variables globales
==================
Dans Plone 3.3, vous avez accès à des variables et fonctions globalement dans vos pages templates. Vous n'y avez pas accès via une vue zope3.
Vous pouvez récupérer une liste des fonctions disponibles dans *Plone-3.3-py2.4.egg/Products/CMFPlone/browser/ploneview.py*.
Toutefois étant donné que dans Plone 4, vous n'y aurez plus accès, prenez l'habitude d'appeler ces fonctions spéciales par l'intermédiaire d'une vue. Par exemple au lieu d'utiliser : ::

    <span tal:content="python:toLocalizedTime(context.ModificationDate())">modification date</span>

utilisez plutôt : ::

    <span tal:define="plone_view context/@@plone"
          tal:content="python:plone_view.toLocalizedTime(context.ModificationDate())">modification date</span>

Les variables globales vont être supprimées dans Plone 4 pour des raisons de performances. En effet de nombreuses variables sont accessibles depuis la template mais ne sont pas forcément utilisées, et donc il y a un traitement inutile au rendu de la page.

Vous avez quatre vues intéressantes pour récupérer des informations :

- @@plone (toLocalizedTime...)
- @@plone_tools (properties pour récupérer portal_properties)
- @@plone_portal_state (navigation_root_url, is_locked, language, is_editable, object_url...)
- @@plone_context_state (portal_url...)


Exercice
========
- Customisation de la template model9 de PloneArticle pour supprimer "ajouter images" et "ajouter liens".

From Raphael Ritz at 
http://n2.nabble.com/where-do-I-find-the-view-template-to-edit-a-page-%28plone-3.2%29-tp2975276p2979777.html :

atct_edit is just a wrapper around base_edit (or whatever gets
called from base_edit) to allow for atct specific form controller
settings without interfering with Archetypes proper.
base_edit in turn pulls in the macros from 'edit_macros' (in
the archetypes skin layer) unless you (or someone) provides
any of those macros specifically (like via a <type_name>_view/edit
template).

http://www.llakomy.com/articles/new-submit-button-for-archetypes-edit-template

