.. ===========================
.. NE MODIFIEZ PLUS CE FICHIER
.. ===========================

.. Les informations figurant dans ce fichier ont été transférées dans
.. sphinx/source/. Ce fichier demeurant en place pour permettre de produire
.. l'ancienne version du document en HTML/PDF.

=====================
Déploiement et backup
=====================

Définition
==========
Le déploiement d'un site Plone requiert des options particulières. Par exemple, nous voulons être sûr qu'une configuration d'un buildout produit la même chose aujourd'hui ou dans un an.

Savoir
======
- Profil buildout de déploiement
- Mettre en place un backup de la ZODB
- Apache
- Varnish
- CacheFu


Profil de déploiement
=====================
Créez un fichier deployment.cfg : ::

    [buildout]
    extends = buildout.cfg

    parts +=
        varnish-build
        varnish

    eggs +=
        Products.CacheSetup

    [varnish-build]
    recipe = zc.recipe.cmmi
    url = ${varnish:download-url}

    [varnish]
    recipe = plone.recipe.varnish
    daemon = ${buildout:parts-directory}/varnish-build/sbin/varnishd
    bind = 127.0.0.1:8000
    backends = 127.0.0.1:${instance:http-address}
    cache-size = 1G
    user = zope

Relancez le buildout avec ``bin/buildout -c deployment.cfg``.

Vous allez créer un utilisateur zope qui servira seulement pour le proxy cache varnish

    $ sudo adduser zope

Pour lancer varnish : ::

    $ sudo -s
    $ bin/varnish

Pour l'arrêter : ::

    $ pkill varnish

Support des backups
===================
Éditez *buildout.cfg*, ajoutez *backup* dans parts : ::

    parts =
        ...
        backup

et ajoutez la section [backup] comme ceci : ::

    [backup]
    recipe = collective.recipe.backup
    keep = 15
    full = true
    gzip = true

Vous avez par défaut les options suivantes : ::

    location = ${buildout-directory}/var/backups
    snapshotlocation = ${buildout-directory}/var/snapshotbackups

`Plus d'informations sur les options de la recipe <http://pypi.python.org/pypi/collective.recipe.backup>`__

Ajoutez ensuite un cronjob (`crontab -e`) pour créer une sauvegarde toute les nuits, ici à 3h du matin : ::

    00 3 * * *      /home/zope/MyProject/bin/backup -q

Pour faire une restauration : ::

    $ bin/restore

Si vous voulez faire un backup de la production pour travailler ensuite en local, utilisez plutôt la commande : ::

    $ bin/snapshotbackup

qui créera une sauvegarde dans le dossier *var/snapshotbackups*, utile pour ne pas perturber les sauvegardes normales qui se font la nuit.
Vous récupérez ensuite la sauvegarde (le fichier fsz et dat) via ``scp`` et vous placez la sauvegarde dans votre dossier *var/backups* en local et exécutez ``bin/restore`` en local.


Configuration d'Apache
======================
Création d'un certificat autosigné : ::

    sudo mkdir -p /etc/apache2/ssl/
    sudo make-ssl-cert /usr/share/ssl-cert/ssleay.cnf /etc/apache2/ssl/server.crt

/etc/apache2/sites-available/kb : ::

    NameVirtualHost 10.56.8.47:80

    <VirtualHost 10.56.8.47:80>
        ServerName devagile
        ServerAdmin anthony.sombris@devagile.fr
        ErrorLog /var/log/apache2/kb_error.log
        TransferLog /var/log/apache2/kb_access.log
        LogLevel warn
        RewriteEngine On
        RewriteRule ^/(.*) https://ssl.devagile/$1 [NC,R=301,L]

    </VirtualHost>

/etc/apache2/sites-available/ssl.kb : ::

    NameVirtualHost 10.56.8.47:443

    <VirtualHost 10.56.8.47:443>
        ServerName ssl.devagile
        ServerAdmin anthony.sombris@devagile.fr
        ErrorLog /var/log/apache2/kb_error.log
        TransferLog /var/log/apache2/kb_access.log
        LogLevel warn

        SSLEngine On
        SSLCertificateFile /etc/apache2/ssl/server.crt
        #SSLCertificateKeyFile /etc/apache2/ssl/server.key

        RewriteEngine On
        RewriteRule ^/(.*) http://localhost:8000/VirtualHostBase/https/%{SERVER_NAME}:443/kb/VirtualHostRoot/$1 [L,P]

    </VirtualHost>

Activez le sites : ::

    a2ensite kb
    a2ensite ssl.kb

Activez les modules : ::

    a2enmod ssl
    a2enmod dav
    a2enmod proxy
    a2enmod proxy_http
    a2enmod rewrite

Éditez */etc/apache2/mods-enabled/proxy.conf* comme ceci : ::

    #Deny from all
    Allow from devagile


Activation de la compression
-----------------------------
Activez le module deflate : ::

    a2enmod deflate

et éditez le fichier de configuration **/etc/apache2/mods-enabled/deflate.conf**
::

  <IfModule mod_deflate.c>
            AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/x-javascript
  </IfModule>


Redémarrez Apache : ::

    /etc/init.d/apache2 restart

configuration des DNS
=====================
Configurer vos DNS ou pour tester en local, éditez /etc/hosts : ::

    10.56.8.47 devagile ssl.devagile

Vous accéderez à votre site à partir de maintenant avec l'adresse *http://devagile**.


Configuration de CacheFu
========================

Allez dans configuration du site -> Cache Configuration Tool et configurez de la manière suivante :

- Cocher Enable CacheFu
- Active Cache Policy: With Caching Proxy
- Proxy Cache Purge Configuration: Purge with VHM URLS
- Site Domains: https://ssl.devagile:443
- Proxy Cache Domains: http://127.0.0..1:8000
- Compression: Never


Ressources
==========

- `Varnish Guru Meditation on timeout`_

.. _`Varnish Guru Meditation on timeout`: http://vincentfretin.ecreall.com/articles/varnish-guru-meditation-on-timeout

Apache et Zope, VirtualHostMonster :

- http://plone.org/documentation/tutorial/plone-apache/vhm/
- http://plone.org/documentation/how-to/plone-with-apache
- http://www.zope.org/Documentation/Books/ZopeBook/2_6Edition/VirtualHosting.stx
- http://wiki.zope.org/zope2/ZopeAndApache

- http://doc.ubuntu-fr.org/tutoriel/securiser_apache2_avec_ssl

Exercice
========
Geler toutes les versions des eggs utilisés dans le buildout.

Ajout de la recipe collective.recipe.backup dans le buildout pour réaliser un backup régulier de la base de données.
