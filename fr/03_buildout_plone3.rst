==========================
Introduction à zc.buildout
==========================

Définition
==========
Un buildout est un dossier contenant plusieurs fichiers de configuration permettant de reproduire à l'identique un environnement de développement ou de production. Paster est l'outil qui permet de générer le code squelette pour démarrer.

Introduction
============
Buildout est un système d'installation permettant d'obtenir le même résultat d'une machine à l'autre. L'installation est reproductible.

- `Qu'est-ce que zc.buildout ?`_
- `Survol de Buildout`_

.. _`Qu'est-ce que zc.buildout ?`: http://ccomb.gorfou.fr/2007/12/13/tutoriel-sur-buildout#qu-est-ce-que-zc-buildout
.. _`Survol de Buildout`: http://ccomb.gorfou.fr/2007/12/13/tutoriel-sur-buildout#survol-de-buildout

zc.buildout permet d'avoir un environnement (pas forcément isolé), mais d'une autre manière que virtualenv.

Une configuration buildout spécifie un ensemble des parts qui peuvent soit être :

- une recipe (recette)
- données de configuration


Organisation d'un buildout
==========================
Un buildout est organisé de la manière suivante :

- *buildout.cfg* : contient la configuration du buildout
- *bootstrap.py* : script d'amorçage de buildout utilisé la première fois
- *src* : par convention, dossier où sont placés les eggs en développement
- *parts* : dossier où sont stockés les données générées des parts si besoin
- *.installed.cfg* : fichier caché mémorisant l'état du buildout
- *eggs* : dossier contenant les eggs activés ou non. Peut ne pas exister si on utilise un dossier partagé pour plusieurs buildout.
- *develop-eggs* : dossier contenant les liens vers les eggs en développement


Nous allons prendre comme exemple le buildout.cfg pour installer archgenxml.
Suivez la `page d'installation du manuel d'archgenxml2`_

.. _`page d'installation du manuel d'archgenxml2`: http://plone.org/documentation/manual/archgenxml2/startup/installation

Créez un dossier *archgenxml_buildout*, placez y une copie du fichier `bootstrap.py`_
et créez un fichier buildout.cfg avec le contenu suivant : ::

    [buildout]
    parts =
        archgenxml

    [archgenxml]
    recipe = zc.recipe.egg:scripts
    eggs = archgenxml

.. _`bootstrap.py`: http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py

Section principale [buildout]
=============================
La variable *parts* contient la liste des parts que buildout doit installer. La convention est de mettre une part par ligne, indenté de 4 espaces. Il peut y avoir des commentaires et des lignes vides.

Chaque part fourni une variable *recipe* pour indiquer comment cette part doit être installé, mis à jour et supprimé.

Il se peut qu'une section ne fournisse pas de recipe. Elle sert généralement pour des données de configuration que d'autres parts utiliseront.

Amorçez le buildout (choisissez bien la version de l'exécutable python) : ::

    $ python bootstrap.py
    Creating directory '/home/vincentfretin/src/archgenxml_buildout/bin'.
    Creating directory '/home/vincentfretin/src/archgenxml_buildout/parts'.
    Creating directory '/home/vincentfretin/src/archgenxml_buildout/eggs'.
    Creating directory '/home/vincentfretin/src/archgenxml_buildout/develop-eggs'.
    Generated script '/home/vincentfretin/src/archgenxml_buildout/bin/buildout'.
    $ tree
    .
    |-- bin
    |   `-- buildout
    |-- bootstrap.py
    |-- buildout.cfg
    |-- develop-eggs
    |   `-- setuptools.egg-link
    |-- eggs
    |   `-- zc.buildout-1.2.1-py2.5.egg
    `-- parts

L'amorçage (ou bootstrapping) installe setuptools et zc.buildout. Ici la version de setuptools du système est utilisé, ce qui explique qu'il est en mode développement. Mais surtout l'amorçage génère le script *bin/buildout*.

Exécutez maintenant : ::

    $ bin/buildout
    Getting distribution for 'zc.recipe.egg'.
    Got zc.recipe.egg 1.2.2.
    Installing archgenxml.
    Getting distribution for 'archgenxml'.
    Got archgenxml 2.4.1.
    Getting distribution for 'stripogram'.
    Got stripogram 1.5.
    ...
    Generated script '/home/vincentfretin/src/archgenxml_buildout/bin/archgenxml'.
    Generated script '/home/vincentfretin/src/archgenxml_buildout/bin/agx_argouml_profile'.
    Generated script '/home/vincentfretin/src/archgenxml_buildout/bin/agx_stereotypes'.
    Generated script '/home/vincentfretin/src/archgenxml_buildout/bin/agx_taggedvalues'.

Le egg archgenxml et ses dépendances sont téléchargés et installés et divers scripts sont générés à la fin.
C'est la recipe qui dit de tout ça.

À première vue, l'exécution de buildout pourrait se résumer à cet algorithme :
pour chaque part de l'option parts de la section [buildout], appeler la recipe associée au part.

Revenons à la ligne ``recipe = zc.recipe.egg:scripts``. *zc.recipe.egg* est un egg à deux namespaces et
le *scripts* après les deux points est un entry point du groupe zc.buildout.

Si vous ne spécifiez pas de point d'entrée, un point d'entrée nommé *default* sera alors recherché dans l'egg.

Jetez un œil au setup.py de zc.recipe.egg : ::

    entry_points = {'zc.buildout': ['default = %s:Scripts' % name,
                                    'script = %s:Scripts' % name,
                                    'scripts = %s:Scripts' % name,
                                    'eggs = %s:Eggs' % name,
                                    'custom = %s:Custom' % name,
                                    'develop = %s:Develop' % name,
                                    ]
                    },

Dans ce cas, nous serions arrivé au même résultat si nous avions mis l'une de ces lignes : ::

    recipe = zc.recipe.egg
    recipe = zc.recipe.egg:default
    recipe = zc.recipe.egg:scripts
    recipe = zc.recipe.egg:script

L'entry point *scripts* pointe vers la classe *Scripts* du package zc.recipe.egg.

Cette classe, comme toute recipe contient une méthode install et update. Voir l'`API des recettes`_

.. _`API des recettes`: http://ccomb.gorfou.fr/2007/12/13/tutoriel-sur-buildout#criture-de-recettes


Le fichier caché *.installed.cfg* garde la configuration de la dernière exécution de buildout.
Lorsqu'une section a été supprimé de la configuration, cette partie sera désinstallée lors de la relance de ``bin/buildout``.
Si une section a été mis à jour, cette partie sera réinstallée.
Pour les nouvelles sections avec recipe, les parties seront installés.

Notre algorithme de tout à l'heure est maintenant : 

- pour chaque part de l'option parts de la section [buildout] :
  
  - installer la recipe du part
  - récupérer l'entry point spécifié ("default" si non spécifié) depuis la recipe.
  - si le part est actuellement installé mais sa configuration a changée, appeler la méthode update de l'entry point
  - si le part n'a pas encore été installé, appeler la méthode install de l'entry point
  - si un part existe dans .installed.cfg et n'est plus dans la liste des parts de [buildout], alors le part est désintallé.


Jetez un œil sur les scripts générés.
Rappel : les scripts archgenxml et agx sont générés car le egg archgenxml a des entry points dans le groupe console_scripts.
::

    $ cat bin/archgenxml
    #!/usr/bin/python

    import sys
    sys.path[0:0] = [
      '/home/vincentfretin/src/archgenxml_buildout/eggs/archgenxml-2.4.1-py2.5.egg',
      '/home/vincentfretin/src/archgenxml_buildout/eggs/stripogram-1.5-py2.5.egg',
      '/home/vincentfretin/src/archgenxml_buildout/eggs/zope.documenttemplate-3.4.2-py2.5.egg',
      '/home/vincentfretin/src/archgenxml_buildout/eggs/zope.component-3.7.0-py2.5.egg',
      '/home/vincentfretin/src/archgenxml_buildout/eggs/zope.interface-3.5.1-py2.5-linux-x86_64.egg',
      '/home/vincentfretin/src/archgenxml_buildout/eggs/xmiparser-1.4-py2.5.egg',
      '/usr/lib/python2.5/site-packages',
      '/home/vincentfretin/src/archgenxml_buildout/eggs/zope.structuredtext-3.5.0dev_plone.2-py2.5.egg',
      '/home/vincentfretin/src/archgenxml_buildout/eggs/zope.event-3.4.1-py2.5.egg',
      ]

    import archgenxml.ArchGenXML

    if __name__ == '__main__':
        archgenxml.ArchGenXML.main()

La première ligne est le shebang, la version du python avec laquelle vous avez fait ``python bootstrap.py`` au début.
archgenxml et toutes ses dépendances sont ajoutés au début du sys.path.

Partage du dossier eggs et downloads
====================================
Lors de l'exécution de buildout, le fichier *~/.buildout/default.cfg* est lu, c'est donc dans ce fichier que nous pouvons mettre des options qui seront partagées par tous nos buildouts.

Le dossier *~/.buildout/* n'existe pas, créez le ainsi que les sous-dossiers : ::

    $ mkdir ~/.buildout ~/.buildout/eggs ~/.buildout/downloads ~/.buildout/configs ~/.buildout/zope

Créez le fichier *~/.buildout/default.cfg* avec ce contenu : ::

    [buildout]
    eggs-directory = /home/vincentfretin/.buildout/eggs
    download-cache = /home/vincentfretin/.buildout/downloads
    extends-cache = /home/vincentfretin/.buildout/configs
    zope-directory = /home/vincentfretin/.buildout/zope

Remplacez ici bien sûr vincentfretin par votre compte. Vous ne pouvez pas utiliser le caractère *~* ici.

À savoir que les valeurs par défaut de ces variables sont : ::
    
    eggs-directory = ${buildout:directory}/eggs
    download-cache = pas précisé, on ne garde pas les archives par défaut
    extends-cache = pas de cache par défaut

${buildout:directory} étant le dossier du buildout.
C'est pour cela que le dossier *eggs* était créé dans le buildout.
Vous pouvez d'ailleurs supprimer ce dossier de votre buildout, il ne sera plus utilisé.

L'option *extends-cache* disponible depuis la version 1.4.0 de zc.buildout permet de mettre en cache les fichiers référencés dans l'option *extends*.
Prenons l'exemple suivant : ``extends = http://dist.plone.org/release/3.3.1/versions.cfg``

Le fichier versions.cfg sera mis en cache dans le dossier *~/.buildout/configs*, le fichier créé étant la somme md5 de l'url.
Une fois mis en cache, il est possible de relancer le buildout en mode hors ligne comme ceci : ``./bin/buildout -o``.

L'option *zope-directory* permet de partager la même installation de Zope pour plusieurs buildouts.

Pinning des versions
====================
À chaque fois que vous exécutez ``bin/buildout``, une requête est faite au serveur central pour savoir si nous avons la dernière version du egg.
C'est le comportement par défaut. En effet nous avons l'option "newest = true" dans la section [buildout] par défaut.

Vous pouvez `bin/buildout -N` pour ne pas vérifier les mises à jour.

Si vous aviez "newest = false" dans votre buildout, la commande `bin/buildout -n` la remettrait à true pour l'exécution.

Le problème est que votre buildout n'est pas reproductible.
Pour qu'il soit reproductible il faudrait que votre buildout quelles versions des eggs doivent être installées.

C'est la qu'intervient l'option *versions* de la section [buildout], vous spécifiez dans quel section vous avez les informations sur les versions.La convention est de l'appeler également versions. Pour pinner (franglais du verbe "to pin" en anglais, participe passé "pinned" en anglais, en français cela pourrait être punaiser, pointer, geler) archgenxml, modifiez votre buildout de cette manière : ::

    [buildout]
    versions = versions
    parts =
        archgenxml

    [versions]
    archgenxml = 2.4.1
    ...

    [archgenxml]
    recipe = zc.recipe.egg:scripts
    eggs = archgenxml

Mais cela ne suffit pas pour que le buildout soit reproducible car nous n'avons pas pinné les dépendances d'archgenxml.

Extension buildout.dumppickedversions
=====================================
zc.buildout peut être étendu avec des extensions. Il y en a eu particulièrement intéressante qui va vous sortir la liste des eggs avec leur version qui ne sont pas pinné.

Une extension s'ajoute avec l'option *extensions* de la section [buildout]
Ajoutez donc l'extension buildout.dumppickedversions à votre fichier *~/.buildout/default.cfg*, comme cela l'extension sera actif pour tous vos buildout : ::

    [buildout]
    extensions = buildout.dumppickedversions
    ...

Relancez ``bin/buildout`` et à la fin de l'exécution vous verrez apparaitre la liste des versions à pinner.
Ajoutez les tous à votre section versions, et reexécuter ``bin/buildout``, il ne devrait plus avoir de versions.


.. _`buildout.dumppickedversions`: http://pypi.python.org/pypi/buildout.dumppickedversions

Il existe aussi une option *allow-picked-versions = false* disponible dans la cœur de zc.buildout qui permet de stopper le buildout si un egg n'est pas pinné.
Cette option et l'extension *buildout.dumppickedversions* sont mutuellement exclusive.


Option extends
==============
Il est possible d'étendre le fichier buildout.cfg.
Vous verrez souvent un fichier deployment.cfg ou development.cfg qui étend le fichier buildout.cfg de base.

Créez un fichier development.cfg : ::

    [buildout]
    extends = buildout.cfg
    parts = omelette

    [omelette]
    recipe = collective.recipe.omelette
    eggs = archgenxml

L'option extends dit de lire le fichier buildout.cfg, et les options que l'on spécifiera par la suite seront écrasées.

Par défaut buildout cherche un fichier buildout.cfg, l'option -c permet d'indiquer un fichier alternatif.

Relancez la machinerie buildout avec ce fichier : ::

    $ bin/buildout -c development.cfg 
    Uninstalling archgenxml.
    Installing omelette.

Oh que c'est-il passé ? Vous avez écrasé l'option parts, il n'y a donc plus que le part omelette à installer.

Vous vouliez garder aussi le part archgenxml, rectifiez ça en transformant le *=* par *+=*, ce qui donne ``parts += omelette``.
Toutes les options supportant une liste fonctionne ainsi (parts, eggs, develop).

Relancez buildout. Là les deux parts sont bien installées.

Remarque : imaginez toujours que vous avez implicitement ``extends = ~/.buildout/default.cfg`` dans votre buildout.cfg de base, à partir duquel vous étendez d'autres configurations, ici c'est le fichier buildout.cfg.


Recipe collective.recipe.omelette
=================================
On ne fait pas d'omelette sans casser des eggs.
Cette recipe permet de mettre à plat les eggs.
::

    [omelette]
    recipe = collective.recipe.omelette
    eggs = archgenxml

Cette recipe génère une arborescence dans parts/omelette : ::

    $ tree parts/omelette/
    parts/omelette/
    |-- archgenxml -> /home/vincentfretin/.buildout/eggs/archgenxml-2.4.1-py2.5.egg/archgenxml
    |-- easy_install.py -> /usr/lib/python2.5/site-packages/easy_install.py
    |-- pkg_resources.py -> /usr/lib/python2.5/site-packages/pkg_resources.py
    |-- setuptools -> /usr/lib/python2.5/site-packages/setuptools
    |-- site.py -> /usr/lib/python2.5/site-packages/site.py
    |-- stripogram -> /home/vincentfretin/.buildout/eggs/stripogram-1.5-py2.5.egg/stripogram
    |-- xmiparser -> /home/vincentfretin/.buildout/eggs/xmiparser-1.4-py2.5.egg/xmiparser
    `-- zope
        |-- __init__.py
        |-- component -> /home/vincentfretin/.buildout/eggs/zope.component-3.7.0-py2.5.egg/zope/component
        |-- documenttemplate -> /home/vincentfretin/.buildout/eggs/zope.documenttemplate-3.4.2-py2.5.egg/zope/documenttemplate
        |-- event -> /home/vincentfretin/.buildout/eggs/zope.event-3.4.1-py2.5.egg/zope/event
        |-- interface -> /home/vincentfretin/.buildout/eggs/zope.interface-3.5.1-py2.5-linux-x86_64.egg/zope/interface
        `-- structuredtext -> /home/vincentfretin/.buildout/eggs/zope.structuredtext-3.5.0dev_plone.2-py2.5.egg/zope/structuredtext

    10 directories, 4 files

Cela permet d'avoir les packages à plat, ce qui facilite la recherche, exemple : ::

    $ find -L parts/omelette -name "interfaces.py"
    $ grep -r "register" parts/omelette


Utilisation de variable
=======================
Vous avez écrit "archgenxml" à deux endroits, une fois dans la recipe zc.recipe.egg et une autre fois dans la recipe collective.recipe.omelette.
Il est plus intéressant de l'indiquer qu'une seule fois dans une variable et d'utiliser cette variable ensuite dans les recipes.

Une convention est de définir une variable *eggs* dans la section [buildout] et de récupérer cette variable avec ${buildout:eggs}.

Voici ce que donne les deux fichiers une fois reécrit.

buildout.cfg : ::

    [buildout]
    versions = versions
    parts =
        archgenxml
    eggs = archgenxml

    [versions]
    archgenxml = 2.4.1
    xmiparser = 1.4
    zc.buildout = 1.2.1
    zc.recipe.egg = 1.2.2
    stripogram = 1.5
    zope.component = 3.7.0
    zope.documenttemplate = 3.4.2
    zope.event = 3.4.1
    zope.interface = 3.5.1
    zope.structuredtext = 3.4.0

    [archgenxml]
    recipe = zc.recipe.egg:scripts
    eggs = ${buildout:eggs}

development.cfg : ::

    [buildout]
    extends = buildout.cfg
    parts += omelette

    [omelette]
    recipe = collective.recipe.omelette
    eggs = ${buildout:eggs}

Vous pouvez référencer n'importe quelle variable de la section que vous souhaitez avec ``${sectionname:variable}``.

Repinning et fusion de section de données
=========================================
Vous voyez que la recipe collective.recipe.omelette n'est pas gelé.
Faites donc les modifications suivantes dans development.cfg : ::

    [buildout]
    ...
    versions = vers

    [vers]
    collective.recipe.omelette = 0.9

Relancez buildout.
Vous voyez que seul collective.recipe.omelette est gelé maintenant car l'option versions a été écrasée.

Renommez "vers" en "versions" et relancez le buildout.

Tous les eggs sont gélés. En effet la section versions de buildout.cfg et la section versions de development.cfg ont fusionné.

En conclusion, nommez toujours *versions* la section contenant les versions. 

Mais maintenir deux listes est source d'erreur.
Créez un fichier versions.cfg qui contient une section [versions] (pas de section [buildout]), et dites à buildout.cfg d'étendre versions.cfg.
Relancez buildout pour voir que tout fonctionne.


L'option develop
================
L'option develop permet d'indiquer quels eggs sont en mode développement.

Créez un dossier src et déplacez y vos deux eggs foo.bar et foo.rab.

Ajoutez foo.bar à l'omelette et relancer ``bin/buildout -c development.cfg``. Buildout tente d'aller chercher foo.bar sur Pypi et échoue.

Nous allons donc lui dire où le trouver.

Ajoutez à la section [buildout] de developement.cfg : ::

    develop =
        src/foo.bar

Relancez ``bin/buildout -c development.cfg``.

Le egg foo.bar est en mode développement : ::

    ls -l develop-eggs/
    total 12
    -rw-r--r-- 1 vincentfretin vincentfretin 57 2009-05-26 18:20 foo.bar.egg-link
    -rw-r--r-- 1 vincentfretin vincentfretin 32 2009-05-26 15:38 setuptools.egg-link

Nous pouvons également utiliser un wildcard dans l'option develop. Mettez ``develop = src/*``,
du coup les deux eggs foo.bar et foo.rab sont en développement.

Option index et find-links
==========================
L'option *index* permet de spécifier un autre index que celui par défaut, par exemple un pypi proxy avec collective.eggproxy.

L'option *find-links* permet d'indiquer des liens supplémentaires où l'on peut trouver les eggs utilisés dans le buildout.

Nous allons maintenant installer foo.bar = 1.0, la release qu'il y a sur notre pypi.
Supprimez donc l'option *develop* et dans development.cfg, ajoutez : ::

    [buildout]
    ...
    find-links += http://devagile:8080/site/products/simple

et dans versions.cfg, ajoutez `foo.bar = 1.0`.


Ordre d'installation des parts
==============================
L'ordre d'installation des parts n'est pas forcément l'ordre donné dans l'option parts de [buildout]. Et une part peut très bien être installée si elle n'est pas listée dans parts.

Modifiez votre buildout.cfg comme ceci : ::

    [buildout]
    ...
    parts =
        zopeskel
        archgenxml

    [archgenxml]
    ...
    packages = ZopeSkel

    [zopeskel]
    recipe = zc.recipe.egg
    eggs = {archgenxml:packages}

L'ordre d'installation sera archgenxml, puis zopeskel.
Si maintenant vous supprimez la part archgenxml de parts, elle sera toujours installée car la part zopeskel en dépend.
