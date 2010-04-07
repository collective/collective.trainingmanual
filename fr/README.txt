.. -*- coding: utf-8 -*-

===========================================
Documentation Plone 3 / Plone 4 en français
===========================================

Installation
============

Si vous êtes déjà familier avec `Sphinx <http://sphinx.pocoo.org/>`_ vous pouvez
passer au chapitre `Règles de rédaction`_. Le présent chapitre présente
l'installation de `Sphinx <http://sphinx.pocoo.org/>`_ et des autres outils
nécessaires à la construction de cette documentation aux formats HTML et PDF.

Python et modules supplémentaires
---------------------------------

Ca va de soi. Il vous faut une installation Python 2.4 ou plus
récente. Attention, Python 3.x n'est pas (encore) supporté.

Installez `distribute
<http://pypi.python.org/pypi/distribute#installation-instructions>`_.

Puis : ::

  $ easy_install virtualenv
  $ easy_install virtualenvwrapper
  $ mkdir ~/.virtualenvs

Ajoutez dans votre .bashrc : ::

  TMPDIR=/tmp
  source /usr/local/bin/virtualenvwrapper.sh

Créez un environnement sphinx et installez Sphinx : ::

  $ mkvirtualenv sphinx
  (sphinx)$ easy_install Sphinx

Si vous avez par la suite des soucis de génération, installez la version 0.6.4
ou ultérieure. La génération du html et pdf fonctionne avec cette version : ::

  (sphinx)$ easy_install Sphinx==0.6.4

.. admonition::
   ``sudo`` ?

   Selon votre installation Python sous Unix (Linux, MacOSX, ...) il vous faudra
   remplacer ``easy_install`` par ``sudo easy_install`` pour l'installation de
   virtualenv et virtualenvwrapper (pas pour Sphinx).

Latex (optionnel)
-----------------

Vous pouvez installer la suite LaTeX minimale pour générer la documentation au
format PDF. N'ayez aucune inquiétude, aucune connaissance de LaTeX n'est requise
pour produire la documentation PDF.

Linux Debian / Ubuntu
.....................

Tout est disponible sous forme de packages pré-compilés : ::

  $ sudo apt-get install texlive

texlive remplace les packages tetex-base tetex-bin tetex-extra, normalement.

MacOSX
......

Si vous avez déjà installé `MacPorts <http://www.macports.org/>`_ (un "must
have" pour tout développeur sous MacOSX), vous n'avez qu'à taper la commande
suivante : ::

  $ sudo port install texlive

Autrement vous pouvez installer le package MacOSX pour votre architecture
(Intel/PPC) à partir du `site TeX Live <http://www.tug.org/texlive/>`_.

Windows
.......

Vous pouvez trouver une distribution et un mode opératoire d'installation TeX
Live pour Windows à partir du `site TeX Live <http://www.tug.org/texlive/>`_.

Attention, vous devrez également disposer de la commande ``make`` qui n'est pas
fournie en standard avec Windows. Vous pourrez vous le procurer soit dans le
bundle `MinGW <http://www.mingw.org/>`_ soit dans le bundle `Cygwin
<http://www.cygwin.com/>`_.

Obtenir et compiler la documentation
====================================

Le référentiel de cette documentation est disponible dans le serveur Subversion
"collective" des contributeurs de Plone. Si vous disposez d'une accréditation
sur ce serveur et désirez devenir contributeur : ::

  $ svn co https://svn.plone.org/svn/collective/collective.trainingmanual/trunk/fr \
    collective.trainingmanual

Si vous ne disposez pas d'accréditation ou voulez juste obtenir et compiler
cette documentation : ::

  $ svn export http://svn.plone.org/svn/collective/collective.trainingmanual/trunk/fr \
    collective.trainingmanual

Vous pouvez maintenant générer cette documentation en HTML : ::

  $ workon sphinx
  (sphinx)$ cd collective.trainingmanual/sphinx
  (sphinx)$ make html

Vous pouvez ouvrir maintenant
``collective.trainingmanual/sphinx/build/html/index.html`` dans votre navigateur
favori.

Pour obtenir la documentation en PDF : ::

  $ workon sphinx
  (sphinx)$ cd collective.trainingmanual/sphinx
  (sphinx)$ make latex
  (sphinx)$ cd build/latex
  (sphinx)$ make all-pdf

Vous pouvez ouvrir maintenant
``collective.trainingmanual/sphinx/build/latex/FormationPlone.pdf`` avec votre
visionneuse PDF favorite (Evince, Acrobat Reader, ...)

Règles de rédaction
===================

Vous devez tout d'abord apprendre les `bases de sphinx
<http://sphinx.pocoo.org/contents.html>`_ qui est un ReStructuredText étendu.

Encodage
--------

Votre éditeur de texte doit encoder le texte en **utf-8** comme celui que vous
êtes en train de lire. Si votre éditeur de texte favori ne reconnait pas cet
encodage (en 2010, ça devient rare), changez d'éditeur.

.. admonition::
   Astuce

   Pour que ``vi``, ``emacs`` et quelques autres éditeurs de texte passent
   automatiquement en utf-8 en ouvrant un fichier pour sphinx, placez en
   première ligne la marque suivante (comme dans le présent fichier) ::

     .. -*- coding: utf-8 -*-

Décalages et indentations
-------------------------

L'utilisation du caractère de tabulation dans le texte source pour les divers
décalages et indentations est **rigoureusement prohibé**. Utlisez toujours des
espaces à cette fin. Tous les éditeurs de textes avancés offrent l'option
d'insérer des espaces lors de l'appui de la touche TAB. Vous n'avez aucune
excuse valable le cas échéant.

Styles de soulignement
----------------------

Sphinx et ReStructuredText n'imposent pas de style de soulignement pour les
différents niveaux de sections d'un document. Tout est laissé à la discrétion
des rédacteurs. Par souci d'homogénéité nous adoptons la convention suivante : ::

  =======================================
  Titre de chapitre (un seul par fichier)
  =======================================
  ...
  Section de niveau 1
  ===================
  ...
  Section de niveau 2
  -------------------
  ...
  Section de niveau 3
  ...................
  ...
  Section de niveau 4
  ~~~~~~~~~~~~~~~~~~~

Il n'est pas utile ou même souhaitable d'aller au delà du niveau 4. Lors de la
génération du document global, le niveau de base des sections d'un fichier
dépend du niveau d'imbrication du fichier dans la structure globale du
document. Pour générer le HTML, ce n'est pas un problème, mais LaTeX limite
l'imbrication des sections à 6 niveaux.

SVN commit
----------

Ouf, vous êtes satisfait de votre excellent document. Il faut en faire profiter
tout le monde. De même que lorsque vous "commitez" du code source, les tests
unitaires ne doivent pas lever d'erreur, vérifiez préalablement :

* Que le ``make html`` ne génère pas d'erreur ou de warning.
* Que vous n'avez pas laissé de faute de frappe.
* Que les liens hypertexte que vous avez ajoutés ou modifiés (glossaire, liens
  externes explicites, références de sections, ...) fonctionnent correctement.

Images
------

Hormis les screenshots - oups, excusez - les copies d'écrans, les images
insérées dans votre document Sphinx doivent être accompagnées de leur version
"source" dans un format public, interopérable et pour lequel un éditeur open
source doit être disponible. Les images doivent être de préférence au format
PNG.

En outre, lors de chaque insertion ou changement d'image, vous **devez**
vérifier et ajuster le cas échéant le rendu PDF, sachant les limitations en
taille des images du au support papier final.

**Exemple :** ::

   .. gs-map.mm: image MindMap des services de GenericSetup. Créé avec FreeMind

   .. image:: gs-map.png

**Applications graphiques recommandées**

Diagrammes : `Graphviz <http://www.graphviz.org/>`_


Quelques outils recommandés
---------------------------

Emacs : vous pouvez ajouter à emacs le module `rst.el
<http://svn.berlios.de/svnroot/repos/docutils/trunk/docutils/tools/editors/emacs/rst.el>`_
qui ajoute la coloration syntaxique et quelques commandes sympathiques aux
rédacteurs de documentation sphinx et reStructuredText.

FAQ
===

**Q :** J'ai ajouté une entrée d'index ou un nouveau terme dans le glossaire ou
fait des modifications de feuille de styles, et ce n'est pas suivi d'effet
lorsque je compile la doc.

**R :** L'index de sphinx est parfois paumée et la gestion des dépendances est
parfois perfectible. Il faut donc tout réinitialiser avec la commande ``make
clean``.
