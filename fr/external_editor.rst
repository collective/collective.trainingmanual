====================
Zope External Editor
====================

Activation du lien External Editor sur le serveur
=================================================
Allez dans la ZMI, portal_memberdata, et cocher l'option ext_editor
Cela activera le lien "Modifier avec une application externe"
à côté des liens "Envoyer cette page" et "Imprimer" sur les documents.

Il y a un bogue dans Plone 3.3.2 qui empêche ce lien de fonctionner.
Éditez
.buildout/eggs/Plone-3.3.2-py2.4.egg/Products/CMFPlone/skins/plone_scripts/external_edit.py
et remplacez ``'%s/externalEdit_/%s.zem'`` par ``'%s/externalEdit_/%s'``.


Problèmes avec l'External Editor
================================
Le problème suivant peut survenir : l'utilisateur clique sur 
"Modifier avec une application externe", il l'édite, sauvegarde et lorsqu'il
reclique sur le lien, il récupère l'ancienne version. Il peut y avoir deux raisons à cela.
Le navigateur n'a pas redemandé le fichier, il l'a pris de son cache.
Ou bien le proxy cache a retourné une version cachée du fichier.

Il semble que l'on ne puisse pas utiliser "Cache-Control:no-cache" à cause de IE.
Voir http://support.microsoft.com/support/kb/articles/q316/4/31.asp

Pour être sûr que le navigateur redemande toujours le fichier, il faut ajouter le header expires à la requête.
Vous pouvez faire cela avec le module *expires* d'apache.

Activez le module comme ceci : ::

    a2enmod expires

Et configurer apache pour que les fichiers avec le type mime application/x-zope-edit
expirent au bout d'une seconde : ::

    sudo vi /etc/apache2/httpd.conf

Ajoutez les lignes : ::

    ExpiresActive On
    ExpiresByType application/x-zope-edit A1

et rechargez apache : ::

    sudo /etc/init.d/apache2 reload

Vous aurez les headers suivants de positionnés : ::

    Cache-Control: max-age=1
    Expires: (last modified date +1s)

Si vous avez le proxy cache varnish, configurez le pour ne pas mettre en cache
les fichiers qui possède le type mime "application/x-zope-edit".
En effet par défaut le fichier est caché pendant 120s, qui est le défaut ttl (time to live).

Pour désactiver cela, ajoutez dans votre varnish.vcl, dans vcl_fetch la règle suivante : ::
        
    if (obj.http.Content-Type == "application/x-zope-edit") {
        pass;
    }

L'utilisateur doit posséder les permission *WebDAV Lock items* et
*WebDAV Unlock items* pour pouvoir verouiller le document via External
Editor.


Installation du client External Editor sous Ubuntu
==================================================
Le système de package d'Ubuntu propose une ancienne version de zopedit.
Nous allons quand même l'installer car il associe le type mime
"application/x-zope-edit" à /usr/bin/zopeedit
Nous allons ensuite remplacer le script par une nouvelle version.

Installez donc zopeedit via le système de packages :
::

    sudo apt-get install zopeedit

Ensuite récupérer la dernière version du script Python zopeedit sur
http://plone.org/products/zope-externaleditor-client

À l'heure actuel, la version stable est la version 0.9.10.

La 0.9.11pre1 est disponible (dans l'encadré à droite) qui ajoute le support
des versions (option désactivé par défaut).

Récupérez le script http://downloads.atreal.net/zopeedit-0.9.11-pre1.py
et remplacez /usr/bin/zopeedit par celui-ci :
::

    sudo cp zopeedit-0.9.11-pre1.py /usr/bin/zopeedit


Supprimez éventuellement l'ancien fichier *~/.zope-external-edit* et
exécutez ``zopedit`` dans un terminal pour recréer un fichier de configuration.

Pour activer le versionning des documents, remplacez:
::

    # Create a new version when the file is closed ?
    # version_control = 0

par :
::

    # Create a new version when the file is closed ?
    version_control = 1

