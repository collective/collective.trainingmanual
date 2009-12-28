==========================================
Création d'un buildout Plone 3 avec paster
==========================================

Installation de Plone
=====================
Note à propos des combinaisons de versions de Plone, Python et Zope :

- Plone 3.3 utilise Python 2.4, Zope 2.10. Python 2.5 et 2.6 ne sont pas supportés.
- Plone 4 utilise Python 2.6 et Zope 2.12.
- Plone trunk utilise Python 2.6 et Zope 2.12.

Installez tout d'abord quelques packages de développement qui seront nécessaires pour compiler PIL (Imaging) et python-libxml2 : ::

    apt-get install libxml2-dev libjpeg62-dev libfreetype6-dev zlib1g-dev

- libxml2-dev pour compiler python-libxml2
- libjpeg62-dev libfreetype6-dev zlib1g-dev pour compiler PIL

Dans Ubuntu Jaunty Jackalope 9.04 et suivants, les versions de Python installés par défaut sont 2.5 et 2.6.
Et les packages python-imaging et python-libxml2 de la distribution ne sont compilés que pour ces versions.
Il n'y a donc plus de support de ces packages pour Python 2.4.
C'est pourquoi ces deux bibliothèques seront compilées à partir du buildout.

`Voir le billet de Maurits van Rees à ce sujet`_

.. _`Voir le billet de Maurits van Rees à ce sujet`: http://maurits.vanrees.org/weblog/archive/2009/03/using-ubuntu-9-04-beta


Installer via buildout généré par ZopeSkel
==========================================
Créez les répertoires buildouts et packages sur le dépôt subversion : ::

    svn mkdir http://devagile/Formation/buildouts
    svn mkdir http://devagile/Formation/packages


Commandes::

    $ paster create -t plone3_buildout plone3 --svn-repository=http://devagile/Formation/buildouts/
    Selected and implied templates:
      ZopeSkel#plone3_buildout  A buildout for Plone 3 projects

    Variables:
      egg:      plone3
      package:  plone3
      project:  plone3
    Enter plone_version (Which Plone version to install) ['3.2.1']: 3.3.X
    Enter zope2_install (Path to Zope 2 installation; leave blank to fetch one) ['']:
    Enter plone_products_install (Path to directory containing Plone products; leave blank to fetch one) ['']:
    Enter zope_user (Zope root admin user) ['admin']:
    Enter zope_password (Zope root admin password) ['']: admin
    Enter http_port (HTTP port) [8080]:
    Enter debug_mode (Should debug mode be "on" or "off"?) ['off']:
    Enter verbose_security (Should verbose security be "on" or "off"?) ['off']:
    Creating template plone3_buildout
    Creating directory ./plone3
      Copying README.txt to ./plone3/README.txt
      Copying bootstrap.py to ./plone3/bootstrap.py
      Copying bootstrap.pyo to ./plone3/bootstrap.pyo
      Copying buildout.cfg_tmpl to ./plone3/buildout.cfg
      Recursing into products
        Creating ./plone3/products/
        Copying README.txt to ./plone3/products/README.txt
      Recursing into src
        Creating ./plone3/src/
        Copying README.txt to ./plone3/src/README.txt
      Recursing into var
        Creating ./plone3/var/
        Copying README.txt to ./plone3/var/README.txt
    -----------------------------------------------------------
    Generation finished
    You probably want to run python bootstrap.py and then edit
    buildout.cfg before running bin/buildout -v

    See README.txt for details
    -----------------------------------------------------------

Vous allez éditer un peu le fichier buildout.cfg avant de l'exécuter.
En effet le fichier généré avec ZopeSkel 2.12 n'est pas suffisant pour Ubuntu 9.04 et 9.10.

Créez un fichier *versions.cfg* et gelez ces versions : ::

    [versions]
    PILwoTk = 1.1.6.4
    libxml2-python = 2.6.21

Dans *buildout.cfg*, modifiez la ligne extends en : ::

    extends =
        versions-plone.cfg
        versions.cfg

Vous allez enregistrer localement le fichier versions.cfg de plone, sinon il est téléchargé à chaque fois que vous faites ``bin/buildout``.

Vous pouvez récupérer le fichier versions.cfg de plonenext 3.3 qui contient les dernières versions de la série 3.3(.x) : ::

    $ wget http://svn.plone.org/svn/plone/plonenext/3.3/versions.cfg -O versions-plone.cfg

Du coup rééditez votre *buildout.cfg*, maintenant l'option extends devient : ::

    extends =
        versions-plone.cfg
        versions.cfg

Remplacez le find-links existant par : ::

    find-links =
        http://dist.plone.org/release/3.3.X
        http://dist.plone.org/thirdparty
        ftp://xmlsoft.org/libxml2/python/libxml2-python-2.6.21.tar.gz

Ajoutez ::

    eggs =
        PILwoTk
        libxml2-python

PILwoTk est téléchargé depuis http://dist.plone.org/thirdparty

La section *productdistros* est utilisée pour installer des produits Zope non encore eggifiés, rare de nos jours.

Notez que la section [zope2] qui utilise la recipe plone.recipe.zope2install a maintenant par défaut fake-zope-eggs=true.

`plus d'informations sur les fake-eggs <http://www.martinaspeli.net/articles/scrambled-eggs>`__


Amorcez et lancez buildout : ::

    $ cd plone3
    $ python2.4 -S bootstrap.py

L'aide de l'option *-S* nous dit *don't imply 'import site' on initialization*,
c'est-à-dire que tous les packages installés globalement dans site-packages ne seront pas dans le sys.path.
Comme cela le package setuptools du système ne sera pas visible et une version récente sera téléchargée et installée dans le buildout.

Continuez : ::

    $ bin/buildout

    $ ls
    bin  bootstrap.py  bootstrap.pyo  buildout.cfg  develop-eggs  fake-eggs  parts  products  README.txt  src  var  versions.cfg
    $ ls parts
    instance  zope2
    $ ls bin
    buildout  instance  repozo  zopepy

- *instance* : script pour contrôler l'instance zope
- *repozo* : script pour faire la sauvegarde de la ZODB
- *zopepy* : shell python avec l'ensemble des eggs

Vérifiez que nos versions de libxml2 et PIL sont bien utilisées : ::

    $ bin/zopepy
    >>> import libxml2
    >>> libxml2.__file__
    '/home/vincentfretin/.buildout/eggs/libxml2_python-2.6.21-py2.4-linux-x86_64.egg/libxml2.pyc'
    >>> import PIL
    >>> PIL.__file__
    '/home/vincentfretin/.buildout/eggs/PILwoTk-1.1.6.4-py2.4-linux-x86_64.egg/PIL/__init__.pyc'

Démarrez l'instance avec ``bin/instance fg`` et connectez vous à http://localhost:8080/manage_main

Créez un Plone Site.

Installation via l'Unified Installer
====================================
Commandes::

    $ wget http://launchpad.net/plone/3.3/3.3.X/+download/Plone-3.3.X-UnifiedInstaller.tgz
    $ tar xvzf Plone-3.3rc3-UnifiedInstaller.tgz
    $ cd Plone-3.3rc3-UnifiedInstaller
    $ ./install.sh --with-python=/usr/bin/python2.4 standalone
    $ cd ~/Plone/zinstance
    $ bin/plonectl start

Le mode standalone crée une seule instance.
Vous pouvez remplacer *standalone* par *zeo* pour créer deux clients avec un zeoserver.

Si vous lancez le script en root, il créera un utilisateur plone et installera Python, Zope et Plone dans /usr/local/Plone.
Python ne sera pas compilé si vous utilisez l'option *--with-python*.

Pour plus d'informations, lisez le fichier README.txt dans l'archive
et la documentation `Installing Plone 3 with the Unified Installer`_ sur plone.org

.. _`Installing Plone 3 with the Unified Installer`: http://plone.org/documentation/tutorial/installing-plone-3-with-the-unified-installer


Installation de produits tierces
================================
Prenons le produit `FCKeditor`_ comme exemple.

Ajoutez Products.FCKeditor dans l'option eggs de la section [instance] et reexécutez buildout.

Démarrez l'instance.

Pour les produits n'étant pas dans le namespace Products, il faut également l'ajouter dans l'option zcml.
À moins que le produit se proclame plugin plone. Dans ce cas-là les fichiers zcml seront inclus grâce à z3c.autoinclude.

.. _`FCKeditor`: http://pypi.python.org/pypi/Products.FCKeditor


Création d'un policy product contenant la configuration du site Plone
=====================================================================
Vous allez créer un *policy product* contenant la configuration du site Plone.

Dans ce policy product, nous allons aussi dire d'installer automatiquement les produits Products.PloneArticle et Products.FCKeditor lors de l'installation du produit.
Nous allons ensuite configurer FCKeditor comme éditeur par défaut pour les utilisateurs nouvellement créés.

Création du policy product
--------------------------
Créez le policy product : ::

    $ cd /tmp/
    $ paster create -t plone formation.policy --svn-repository=http://devagile/Formation/packages
    $ cd formation.policy
    $ svn rm --force formation.policy.egg-info
    $ svn ci -m"Add initial structure for formation.policy"

Le template *plone* hérite du template *basic_namespace*, il ajoute en plus un fichier configure.zcml.

utilisation de svn:externals pour faire une sorte de checkout dans le dossier src : ::

    $ cd ~/workspace/plone3/src/
    $ vim EXTERNALS.txt
    formation.policy http://devagile/Formation/packages/formation.policy/trunk
    $ svn propset svn:externals -F EXTERNALS.txt .
    $ svn up
    $ svn add EXTERNALS.txt
    $ svn ci -m"Set svn:externals on src directory to install formation.policy"

Ajoutez Products.PloneArticle et Products.FCKeditor en dépendances de formation.policy dans le fichier *src/formation.policy/setup.py* (option install_requires).

Lorsque vous êtes dans le dossier src, la commande ``svn stat`` vous renvoie les changements fait dans les externals,
ici les changements de formation.policy s'il y en a.
La commande ``svn up`` sera également fait dans les différents externals.
La seule exception est la commade ``svn ci`` exécutée à partir du dossier *src* ou plus en amont, les fichiers modifiés ou ajoutés dans les externals ne seront pas commités.
Il faut vraiment être à l'intérieur de l'external, ici le dossier *formation.policy* pour que le commit des changements soit réalisé.

Ceci dit, commitez le changement fait au fichier setup.py.

Editez buildout.cfg pour ajouter formation.policy : ::

    [buildout]
    ...
    develop += src/formation.policy

    [instance]
    ...
    eggs =
        ...
        formation.policy
        Products.PloneArticle
        Products.FCKEditor
    zcml =
        formation.policy

Bien que les produits Products.PloneArticle et Products.FCKEditor soient des dépendances de formation.policy et qu'ils vont donc être installés,
il est nécessaire de les remettre dans l'option eggs pour qu'ils apparaissent dans le sys.path du script *bin/instance*. Bogue de la recipe zc.recipe.egg ?

Exécutez *bin/buildout*.

L'ajout de formation.policy dans l'option *zcml* génère un *ZCML slug*,
fichier XML contenant une seule ligne : ::

    $ cat parts/instance/etc/package-includes/001-formation.policy-configure.zcml
    <include package="formation.policy" file="configure.zcml" />

En fait au démarrage de l'instance Zope, le fichier *parts/instance/etc/site.zcml* est lu,
ce qui entraine la lecture de tous les fichiers situés dans le dossier *package-includes*,
ainsi que les fichiers meta.zcml, configure.zcml et overrides.zcml des produits dans le namespace Products.

La chaine de lecture est donc celle-ci :

- parts/instance/etc/site.zcml
- parts/instance/etc/package-includes/001-formation.policy-configure.zcml
- src/formation.policy/formation/policy/configure.zcml

Ces fichiers ZCML sont les fichiers de configuration utilisés par la machinerie Zope 3 pour enregistrer les composants au démarrage.

Installation de Products.PloneArticle à l'installation de formation.policy
--------------------------------------------------------------------------
Vous allez maintenant dire à Plone d'installer Products.PloneArticle lorsque vous installez formation.policy.

Éditez le fichier *src/formation.policy/formation/policy/configure.zcml* comme ceci : ::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        i18n_domain="formation.policy">

        <five:registerPackage package="." />

        <genericsetup:registerProfile
          name="default"
          title="formation Policy"
          directory="profiles/default"
          description="Turn a Plone site into the formation site."
          provides="Products.GenericSetup.interfaces.EXTENSION"
          />

    </configure>

La directive *five:registerPackage* signale à Zope que c'est un produit. Cette ligne est importante vu que nous ne sommes pas dans le namespace Products.

La directive *genericsetup:registerProfile* permet d'enregistrer un nouveau profile d'extension (option *provides*) avec le nom "default" (option *name*).
Les fichiers du profile se trouvent dans le dossier *profiles/default* (option *directoy*).

Créez le dossier *profiles/default* et créez le fichier *metadata.xml* comme ceci : ::

    <?xml version="1.0"?>
    <metadata>
      <version>1</version>
      <dependencies>
        <dependency>profile-Products.PloneArticle:default</dependency>
      </dependencies>
    </metadata>

Le produit PloneArticle utilise bien un profile donc nous pouvons l'installer de cette manière.

Jetez un œil à la seule documentation qui existe sur le `support des dépendances de produits dans metadata.xml`_.

Notez que la *best practice* est maintenant d'utiliser un entier pour la version du profile : 1, 2, 3 etc.
Avec ArchGenXML 2.4.1, il faut au moins deux entiers séparés par un point, ex : 1.0. Ce sera sans doute corrigé dans une prochaine version.

Dans la chaine *profile-Products.PloneArticle:default*, nous avons le préfixe *profile-*, le package au sens Python *Products.PloneArticle*, le caratère *:* et le nom du profile à charger *default*.
Ici *default* est le *name* donné lors du *genericsetup:registerProfile* dans le fichier configure.zcml de Products.PloneArticle.

.. _`support des dépendances de produits dans metadata.xml`: http://plone.org/products/plone/roadmap/195


Déclaration de formation.policy comme plugin Plone
--------------------------------------------------
Plone 3.3 inclu un nouveau `système de plugin`_. Un produit peut être déclaré plugin Plone.
Dans ce cas les fichiers meta.zcml, configure.zcml et overrides.zcml du produit seront lus au démarrage, comme pour les produits dans le namespace Products.
Il n'est plus nécessaire d'ajouter le produit dans l'option *zcml* de la section [instance] dans buildout.cfg.

.. _`système de plugin`: http://plone.org/products/plone/roadmap/247

Pour cela vérifiez que le egg est déclaré comme plugin plone, avec dans *src/formation.policy/setup.py* : ::

    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """

Supprimez formation.policy de l'option *zcml* de la section [instance] dans buildout.cfg.

Et relancez ``bin/buildout`` qui va supprimer le fichier *parts/instance/etc/package-includes/001-formation.policy-configure.zcml*.
La commande regénère également les metadonnées associées aux eggs en développement,
concrètement il regénére le fichier *src/formation.policy/formation.policy.egg-info/entry_points.txt* qui déclare le egg comme plugin Plone.


À quel moment est lu le fichier configure.zcml de formation.policy ? Il n'y a rien de magique, la chaine de lecture est maintenant :

- parts/instance/etc/site.zcml
- lecture des fichiers configure.zcml de tous les produits dans le namespace Products
- ~/.buildout/eggs/Plone-3.3rc3-py2.4.egg/Products/CMFPlone/configure.zcml
  qui contient les lignes : ::

      <!-- include plone plugins with z3c.autoinclude -->
      <includePlugins package="plone" file="configure.zcml" />

  includePlugins est une nouvelle directive fourni par z3c.autoinclude.
  Ici tous les eggs ayant un entry point dans le groupe *z3c.autoinclude.plugin* sont recherchés.
  Nous avons dans cette directive *package="plone"* donc seul les entry points avec *target = plone* sont gardés.
  Pour chaque eggs, le fichier configure.zcml (option *file* de la directive) est lu.
- src/formation.policy/formation/policy/configure.zcml

Vous avez le même principe pour les fichiers meta.zcml et overrides.zcml, jetez un œil dans Products/CMFPlone/meta.zcml et Products/CMFPlone/overrides.zcml.

Installation de Products.FCKeditor à l'installation de formation.policy
--------------------------------------------------------------------------
Pour dépendre de FCKeditor, nous ne pouvons pas utiliser cette méthode car FCKeditor n'utilise pas de profile, mais l'ancien dossier Extensions pour être installé via portal_quickinstaller.

Il existe un produit pour installer des vieux produits à partir d'un profile : `genericsetup.quickinstaller`_.
Ce produit enregistre un nouvel *importStep* dans *portal_setup* qui regarde lors de l'installation d'un produit s'il existe un fichier  *products.xml* dans le dossier du profile.
Pour que cela marche, il faut que le fichier configure.zcml de genericsetup.quickinstaller soit lu d'une manière ou d'une autre au démarrage.

Ajoutez *genericsetup.quickinstaller* dans setup.py install_requires du policy product.

Il faut donc lire le fichier configure.zcml du produit genericsetup.quickinstaller, vous pouvez ajouter dans *src/formation.policy/formation/policy/configure.zcml*, cette directive : ::

    <include package="genericsetup.quickinstaller" />

Ici l'option *file* n'est pas précisée, la valeur par défaut étant *file="configure.zcml"*.

L'inconvénient de cette ligne est que vous avez l'information genericsetup.quickinstaller à deux endroits, une première fois dans le fichier setup.py et une deuxième fois dans configure.zcml.

Plone 3.3 inclu le package z3c.autoinclude qui permet de ne pas se répéter.
En lieu et place de la ligne ci-dessus, vous pouvez utiliser celle-ci : ::

    <includeDependencies package="." />

Cette directive recupère la liste des dépendances du egg.
Petit rappel, il le récupère à partir du fichier *src/formation.policy/formation.policy.egg-info/requires.txt* qui lui a été généré à partir des informations de setup.py.
Pour chaque dépendance dans l'ordre déclaré, elle va inclure dans l'ordre les fichiers meta.zcml, configure.zcml et overrides.zcml s'ils existent.

Pour finir, créez un fichier *profiles/default/products.xml* qui sera lu par l'importStep enregistré par genericsetup.quickinstaller : ::

    <?xml version="1.0"?>
    <products>
      <installs>
        <product name="FCKeditor" />
      </installs>
    </products>

.. _`genericsetup.quickinstaller`: http://pypi.python.org/pypi/genericsetup.quickinstaller


Configuration de FCKeditor pour tous les nouveaux utilisateurs
--------------------------------------------------------------
Vous allez configurer FCKeditor comme éditeur par défaut (seulement effectif pour les nouveaux utilisateurs).
Allez dans la ZMI, dans *portal_memberdata*, cliquez sur l'onglet *Properties*.
Éditez la propriété *wysiwyg_editor*, mettez la valeur *FCKeditor*.

Maintenant vous allez exporter cette configuration dans votre policy product.
Allez dans la ZMI, *portal_setup*, onglet *Export*, sélectionnez le step *MemberData properties*, et cliquez sur *Export selected steps*.

Téléchargez l'archive tar.gz proposée, extrayez son contenu dans un dossier temporaire
et copiez le fichier *memberdata_properties.xml* dans le dossier profiles/default de votre policy product.

Éditez le fichier pour ne laisser que la propriété qui vous intéresse.
Vous devez donc avoir au final un fichier *profiles/default/memberdata_properties.xml* avec ce contenu : ::

    <?xml version="1.0"?>
    <object name="portal_memberdata" meta_type="PlonePAS MemberData Tool">
     <property name="wysiwyg_editor" type="string">FCKeditor</property>
    </object>

Vous pouvez exporter de cette façon presque la totalité des configurations des tools Plone.

Comme vous avez ajouté un fichier dans le profile, incrémentez la version dans metadata.xml.

Pour être sûr que l'import fonctionne bien, remettez wysiwyg_editor=Kupu depuis la ZMI, reinstallez formation.policy, wysiwyg_editor devrait maintenant être FCKeditor.


En exercice : installez `Products.SmartPrintNG`_ qui permet de générer un pdf d'un document Plone.

.. _`Products.SmartPrintNG`: http://pypi.python.org/pypi/Products.SmartPrintNG


À propos des versions
=====================
La page *Produits d'extension* accessible via *Configuration du site* est une interface à portal_quickinstaller et portal_setup.
Elle permet d'installer les produits n'ayant pas de profile avec portal_quickinstaller et les produits avec profile avec portal_setup.

Les versions affichées sont ceux des eggs.
La version est récupérée via le module pkg_resources fourni par setuptools comme vu précédemment.

La version du egg et du profile peuvent être différentes. Il est même conseillé dès le départ d'utiliser des versions différentes pour la version du produit/egg, et la version du profile.

La version du egg est une version de la forme 1.0.0, 1.0.1, 1.1.0 etc. Si vous modifiez du code Python, incrémentez cette version.

La version du profile est un simple entier qui est incrémenté à chaque fois qu'un fichier est modifié ou ajouté dans le dossier du profile. Vous incrémenterez généralement aussi la version du egg.

Releaser le policy product
==========================
Maintenant que vous avez un policy product qui fait quelque chose, il est peut-être temps de réaliser une release pour pouvoir l'utiliser en production.
En effet il n'est pas conseillé d'utiliser des produits en mode développement en production.

La première chose à faire et d'éditer le changelog dans le fichier *docs/HISTORY.txt*.
Ce fichier texte est au format reST (`reStructuredText`_). Il faut respecter certaines convention d'écriture pour que ce fichier puisse être généré ensuite en HTML sur Pypi.

- le soulignage d'un titre doit aller exactement jusqu'au bout du titre.
- les listes doivent avoir une ligne vide au début et à la fin

.. _`reStructuredText`: http://docutils.sourceforge.net/rst.html

Pour cette première release, vous allez seulement spécifier la date de la release. Remplacez juste *Unreleased* par *2009-06-11*.
Remplacez également la puce de la liste, l'étoile par un tiret qui est la convention dans les produits plone.

Votre fichier doit ressembler à ceci : ::

   Changelog
   =========

   1.0 - 2009-06-11
   ----------------

   - Initial release

La version dans setup.py doit également être *1.0*.

Commitez : ::

    $ svn ci -m"Prepare release"

Maintenant vous allez faire un tag, c'est-à-dire une copie d'une branche qui sera gelée, faire un checkout de ce tag et pousser la release ::

    $ svn cp http://devagile/Formation/packages/formation.policy/trunk http://devagile/Formation/packages/formation.policy/tags/1.0 -m"Tagged"
    $ cd /tmp
    $ svn co http://devagile/Formation/packages/formation.policy/tags/1.0
    $ cd 1.0/
    $ python setup.py egg_info -RDb "" mregister sdist --formats=zip mupload -r mycompany

Il y a aussi une autre manière de faire, au lieu de préciser *egg_info -RDb ""*, vous pouvez supprimer le fichier *setup.cfg*, commiter et faire la release sans préciser *egg_info -RDb ""*.

Retournez ensuite dans le trunk (dossier *src/formation.policy/*), incrémentez la version dans *setup.py*, donc ici *1.1*. Et éditez le changelog comme ceci : ::

   Changelog
   =========

   1.1 - unreleased
   ----------------

   1.0 - 2009-06-11
   ----------------

   - Initial release

Et commitez : ::

    $ svn ci -m"Update version after release"

Vous allez dorénavant utiliser cette version releasé plutôt que le egg en développement.

Supprimez *formation.policy* de l'option *develop* de la section [buildout] dans *buildout.cfg*.

Ajoutez aussi le lien vers le Pypi dans find-links : ::

    [buildout]
    find-links +=
        ...
        http://ip:8080/site/products/simple

Précisez la version *formation.policy = 1.0* dans *versions.cfg*.

L'external ne sera plus utilisé dans la suite, donc supprimez le également : ::

    $ svn rm src/EXTERNALS.txt
    $ svn propdel svn:externals src/
    $ svn ci -m"Removed external"


Pour plus d'informations sur comment faire une release, voyez les liens suivants :

- http://grok.zope.org/documentation/how-to/releasing-software
- http://plone.org/documentation/tutorial/how-to-upload-your-package-to-plone.org


Vous pouvez maintenant mettre à jour votre serveur de production.
Il est recommandé de créer une branche production de votre buildout trunk.
De cette manière vous saurez à tout moment quelle version vous avez en production.

Créez la branche : ::

    $ svn cp http://devagile/Formation/buildouts/plone3/trunk http://devagile/Formation/buildouts/plone3/branches/production -m"Created production branch"

Sur le serveur, initialement vous avez réalisé un checkout de la branche production : ::

    $ svn co http://devagile/Formation/buildouts/plone3/branches/production plone3
    $ cd plone3
    $ python2.4 -S bootstrap.py
    $ bin/buildout
    $ bin/instance start

Pour les prochaines mises à jour en production, seulement les commandes suivantes sont nécessaires : ::

    $ cd plone3
    $ svn up
    $ bin/buildout
    $ bin/instance restart


Repasser au développement
=========================
Maintenant vous voulez repasser le egg formation.policy en mode développement pour travailler dessus. Il faut :

- supprimer la version dans versions.cfg
- ajouter le egg dans l'option develop de buildout.cfg
- reconfigurer l'external pour récupérer le egg dans le dossier src

Passer du mode développement au mode production et vice-versa génère beaucoup de bruit dans les logs svn,
mais surtout il faut sans cesse répéter les mêmes actions.

Nous allons utiliser dans la suite une extension buildout nommée *mr.developer* qui s'occupe de réaliser les 3 étapes décrites ci-dessus en une commande.


Utilisation de mr.developer pour gérer les composants en développement
======================================================================
L'extension pour zc.buildout `mr.developer`_ permet de gérer les composants en développement.

Transformez le fichier buildout.cfg : ::

    extends =
        ...
        sources.cfg
    extensions +=
        ...
        mr.developer

Créez le fichier *sources.cfg* avec ce contenu : ::

    [buildout]
    auto-checkout =
        formation.policy

    [sources]
    formation.policy = svn http://devagile/Formation/packages/formation.policy/trunk

Exécutez ``bin/buildout`` et mr.developer va s'occuper de faire un checkout de formation.policy dans le dossier src.
L'extension s'occupe aussi de passer en mode développement formation.policy et de supprimer formation.policy de versions.cfg pour que ce soit bien
la version en développement qui soit utilisée. Cela est fait de manière interne, les fichiers ne sont pas touchés.

mr.developer génère le script ``bin/develop`` qui est un script à tout faire.
Exécutez ``bin/develop help`` pour obtenir la liste des commandes, qui ressemblent beaucoup à subversion.

``bin/develop stat`` vous liste les checkouts du dossier src/, vous dit s'ils sont actifs ou non (c'est-à-dire en mode développement ou non)
et s'ils sont dans l'option *auto-checkout* ou non. Exécutez ``bin/develop help stat`` pour obtenir la légende.

``bin/develop co plonetheme.formation`` fait un checkout dans le dossier src, et active le egg (le met en mode développement).

``bin/develop activate plonetheme.formation`` suivit de ``bin/buildout`` permet de passer le egg en mode développement.

``bin/develop deactivate plonetheme.formation`` suivit de ``bin/buildout`` permet de désactiver le mode développement et d'utiliser la version spécifié dans versions.cfg.

``bin/develop up -vf`` permet de mettre à jour tous les checkouts. L'option *-v* permet d'afficher les messages de subversion.
L'option *-f* permet de forcer un *svn up* si le checkout est dans un état pas clean.

L'idée est d'ajouter dans auto-checkout les eggs qui ont été modifiés après leur dernière release.
Comme ceci lorsqu'il est temps de livrer votre travail en production, vous savez exactement quels sont les eggs dont vous devez faire une release.

.. _`mr.developer`: http://pypi.python.org/pypi/mr.developer


Mettre à jour la branche de production
======================================
Vous avez commité un changement dans le trunk, il faut le backporté dans la branche production.
Le commit sur le trunk est la révision 1023, pour merger ce commit sur la branche de production : ::

    trunk$ svn info
    URL : <url_to_repository>/trunk
    trunk$ cd ../branches/production
    branches/production$ svn merge -c 1023 <url_to_repository>/trunk .

Puis il faut commiter le résultat en précisant dans le message les numéros de versions et leur origine : ::

    branches/production$ svn info
    ...
    Révision : 1025
    ...
    branches/production$ svn ci -m"Merged -r1023:1025 from trunk"


Connaitre les révisions mergées
-------------------------------
Sur un serveur subversion >= 1.5 seulement : ::

   branches/production$ svn mergeinfo <url_to_repository>/trunk .

Connaitre les révisions à merger
--------------------------------
Sur un serveur subversion >= 1.5 seulement : ::

   branches/production$ svn mergeinfo --show-revs eligible <url_to_repository>/trunk .


Fabric
======
Créez un environnement isolé Python 2.5 ou 2.6 avec Fabric d'installé : ::

    $ mkvirtualenv -p /usr/bin/python2.5 --no-site-packages fab
    (fab)$ easy_install http://git.fabfile.org/cgit.cgi/fabric/snapshot/fabric-0.9a3.tar.gz

Création d'un script Fabric pour la maintenance de l'instance Plone à distance.
Créez un fichier *fabfile.py* à la racine de votre buildout : ::

    from fabric.api import run, sudo, env, hosts

    env.user = "anthony"
    env.hosts = ('devagile',)

    def update():
        """Update the checkout of the buildout
        """
        run("cd /home/anthony/workspace/plone3; svn up")

    def restart():
        """Restart the instance
        """
        run("/home/anthony/workspace/plone3/bin/instance restart")

    def stop():
        """Stop the instance
        """
        run("/home/anthony/workspace/plone3/bin/instance stop")

    def start():
        """Start the instance
        """
        run("/home/anthony/workspace/plone3/bin/instance stop")

    def buildout():
        """Run bin/buildout
        """
        run("cd /home/anthony/workspace/plone3; bin/buildout")

    def up_and_restart():
        """Update the checkout and restart the instance
        """
        update()
        restart()

    def full_up_and_restart():
        """Do the actions stop, update, buildout, start
        """
        stop()
        update()
        buildout()
        start()

Pour afficher la liste des commandes disponibles : ::

    $ fab --list
    Available commands:

        buildout             Run bin/buildout
        full_up_and_restart  Do the actions stop, update, buildout, start
        restart              Restart the instance
        start                Start the instance
        stop                 Stop the instance
        up_and_restart       Update the checkout and restart the instance
        update               Update the checkout of the buildout

Pour redémarrer l'instance : ::

    $ fab restart

Pour préciser un autre host qui va donc écraser le host configuré globalement dans le fichier : ::

    $ fab stop:host=ailleurs

Vous pouvez aussi créer des commandes avec des paramètres, exécutez ``fab -h`` pour consulter la liste des options.

Pour plus de détails, consulter la `documentation de Fabric`_

.. _`documentation de Fabric`: http://docs.fabfile.org/#documentation

Ressources
==========
- http://plone.org/documentation/tutorial/buildout
- http://www.sixfeetup.com/swag/buildout-quick-reference-card
