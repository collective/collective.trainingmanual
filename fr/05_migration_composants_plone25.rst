.. ===========================
.. NE MODIFIEZ PLUS CE FICHIER
.. ===========================

.. Les informations figurant dans ce fichier ont été transférées dans
.. sphinx/source/. Ce fichier demeurant en place pour permettre de produire
.. l'ancienne version du document en HTML/PDF.

==================================================
Migration des composants développés pour Plone 2.5
==================================================

Définition
==========
La façon d'écrire un produit Plone a complètement changé entre la version 2.5 et 3. Les workflows ne sont plus écrit en Python, mais en XML. Plone 3 privilégie plus un développement à la Zope 3.

Savoir
======
- Migration des anciens modèles UML vers la dernière version de ArgoUML
- Génération de code avec la dernière version de ArchGenXML
- Migration du code de l'ancien composant vers le nouveau composant

Outils
======
Sous Ubuntu pour comparer deux dossiers, on peut utiliser kompare (non éditable) ou meld (éditable) : ::

    $ sudo apt-get install kompare meld

Pour utiliser *meld* par exemple : ::

    $ meld dossier1 dossier2

Outils pour la preview des documents
====================================
Pour le support de la prévisualisation des documentations avec ARFilePreview et AROfficeTransforms : ::
    
    $ sudo apt-get install wv poppler-utils ppthtml xlhtml pstotext unrtf

Installation du produit AttachmentField
=======================================

Éditez le fichier buildout.cfg comme ceci : ::

    [buildout]
    parts =
        ...
        productdistros

    [instance]
    products =
        ...
        ${productdistros:location}

    [productdistros]
    # For more information on this step and configuration options see:
    # http://pypi.python.org/pypi/plone.recipe.distros
    recipe = plone.recipe.distros
    urls = http://plone.org/products/attachmentfield/releases/1.4.4/attachmentfield-1-4-4.tgz
    nested-packages =
    version-suffix-packages =


Génération du produit AgileKnowledgeBase
=========================================
Tout d'abord générez le produit AgileKnowledgeBase avec la dernière version de ArchGenXML.

Vincent fait un checkout : ::

    $ svn co --username vincent http://devagile/Agile
    $ cd Agile

Anthony fait un checkout, crée et commit un dossier packages : ::

    $ svn co --username anthony http://devagile/Agile
    $ cd Agile
    $ svn mkdir packages
    $ svn ci -m"Add new packages directory"

Vincent fait un update : ::

    $ svn log -v 
    ------------------------------------------------------------------------
    r1 | anthony | 2009-06-04 14:51:20 +0200 (jeu 04 jun 2009) | 1 line
    Chemins modifiés :
       A /packages

    add new packages directory
    ------------------------------------------------------------------------

Anthony fait : ::

    $ cd /tmp
    $ paster create -t basic_namespace Products.AgileKnowledgeBase --svn-repository=http://devagile/Agile/packages/
    $ cd Products.AgileKnowledgeBase
    $ svn stat
    $ svn rm --force Products.AgileKnowledgeBase.egg-info
    $ svn ci -m"Add skeleton"
    $ cd projet/packages
    $ svn up
    $ cd Products.AgileKnowledgeBase/trunk
    $ svn mkdir model
    $ svn ci -m"Added a model directory"

Copiez-collez le fichier zargo dans ce dossier model et ajoutez le à svn : ::
    
    $ svn add model/AgileKB.zargo
    $ svn ci -m"Added zargo model"

    $ cd Products
    $ archgenxml ../model/AgileKB.zargo

Note : sous Windows les images sont générées bizarrement.

Éditez le fichier profiles/default/types.xml pour changer le meta_type du type d'agile_document : ::

    <object name="agile_document"
            meta_type="Factory-based Type Information for Plone Articles content types"/>

Vous devrez faire attention à garder ce changement à chaque fois que vous regénèrerez le modèle.

Mettez "1.0" pour la version dans profiles/default/metadata.xml : ::

    $ svn add AgileKnowledgeBase/*
    $ svn ci -m"Add generated code"

Ajoutez Products.PloneArticle dans install_requires de setup.py
Dans profiles/default/metadata.xml : ::

    <?xml version="1.0"?>
    <metadata>
      <version>1</version>
      <dependencies>
        <dependency>profile-Products.PloneArticle:default</dependency>
      </dependencies>
    </metadata>

Ajoutez Products.PloneArticle dans l'option eggs de la section [instance] sinon il ne sera pas dans le sys.path du script *bin/instance*

Configuration du calendrier
===========================
Il faut ajouter le type agile_event dans portal_calendar pour que les évènements s'affichent dans le calendrier.

Création d'un nouveau Plone Site
================================
Créez un nouveau Plone Site, installez les produits.

Migration du contenu
====================
Sur le serveur en production :

- Passer le storage de FSS en AttributeStorage
- Faire un export au format zexp de acl_users, portal_memberdata, portal_groupdata, aide, dossiers des espaces
- Copier les logs

Sur le nouveau serveur :

- copier tous les zexp dans le dossier *parts/instance/import/*
- copier les logs en les renommant
- importer les utilisateurs :

  1. Go to your new site and Delete the following objects (all relative to the Plone site root):

   * acl_users -> Contents -> local_roles
   * acl_users -> Contents -> mutable_properties
   * acl_users -> Contents -> portal_role_manager
   * acl_users -> Contents -> source_groups
   * acl_users -> Contents -> source_users
   * portal_groupdata
   * portal_memberdata

  2. Copy the corresponding objects from the old site and paste it into the new one at the same location.
  3. For the 5 new objects in acl_users go to their Activate tab and activate them (check all checkboxes and click on Update). 
  4. Cut & paste Members' content

- importer les espaces
- Aller dans plonearticle_tool et faire la migration en sélectionnant la version 4.0.0rc2

Ajout nouvelles fonctionnalités
===============================
Prévisualisation des documents Word et PDF
------------------------------------------
`ARFilePreview`_ est un produit qui ajoute la prévisualisation des documents Word et PDF.
Vous pouvez installer le produit `AROfficeTransforms`_ pour installer des transformations pour Excel et OpenOffice.org.

La dernière release de ARFilePreview sur plone.org est assez vieille, donc vous allez télécharger la dernière version de la branche v2.
(La branche v2 fonctionne avec portal_transforms, le trunk (v3) fonctionne avec plone.transforms.)
Pour cela, vous allez utiliser la recipe `infrae.subversion`_ pour faire un checkout du produit : ::

    [buildout]
    parts =
        ...
        development-products

    [development-products]
    recipe = infrae.subversion
    urls =
        http://svn.plone.org/svn/collective/ARFilePreview/branches/ARFilePreview-v2@88162 ARFilePreview
    location = products

Il faut que vous ayez la section productdistros d'activée pour que le produit soit pris en compte au démarrage.

.. _`infrae.subversion`: http://pypi.python.org/pypi/infrae.subversion
    
Pour installer AROfficeTransforms, ajoutez l'url de l'archive dans la section productdistros : ::
    
    [productdistros]
    ...
    urls = 
        ...
        http://plone.org/products/arofficetransforms/releases/0.9.2/arofficetransforms-0-9-2.tgz


Génération de pdf
-----------------
Installez Products.SmartPrintNG.

Pour générer les pdfs, SmartPrintNG a besoin de ``fop`` : ::

    $ apt-get install fop

Dans la section [instance], ajoutez : ::

    environment-vars =
        FOP_HOME /usr/bin

fop cherche la librairie Java servlet-api.jar. Vous pouvez rechercher dans quel package Ubuntu il se trouve avec ``apt-file search``.

Tout d'abord installez la commande apt-file et mettez à jour la base de données : ::

    $ sudo apt-get install apt-file
    $ sudo apt-file update

Cherchez où se trouve ce fichier : ::

    $ apt-file search servlet-api.jar
    eclipse-platform: /usr/lib/eclipse/plugins/org.eclipse.tomcat_5.5.17/lib/servlet-api.jar
    groovy: /usr/share/groovy/lib/servlet-api.jar
    libservlet2.4-java: /usr/share/java/servlet-api.jar
    libtomcat5.5-java: /usr/share/tomcat5.5/common/lib/servlet-api.jar
    tomcat6: /var/lib/tomcat6/lib/servlet-api.jar
    tomcat6-common: /usr/share/tomcat6/lib/servlet-api.jar

Installez le package voulu : ::

    $ sudo apt-get install libservlet2.4-java


Exercice
========
Migration du composant « base de connaissances » comme cas pratique.
