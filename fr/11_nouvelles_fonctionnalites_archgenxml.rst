=======================================
Nouvelles fonctionnalités de ArchGenXML
=======================================

Définition
==========
La dernière version de ArchGenXML permet de modéliser plus de chose que dans les versions précédentes.

Savoir
======
- modélisation des portlets
- modélisation des vues zope 3


Modélisation d'un portlet
=========================
Créez un package portlets et créez une classe avec le stéréotype portlet_class.

Modélisation de vue zope 3
==========================
Regardez le modèle de Products.rendezvous sur pypi : ::

    $ cd /tmp/
    $ easy_install -b. -e Products.rendezvous

Ouvrez le modèle /tmp/products.rendezvous/model/rendezvous.zargo avec ArgoUML.

Procédure :

- Créez un package browser, ajoutez y une classe MyView avec le stéréotype view_class. Vous pouvez préciser le stéréotypes name "myview" et permission "cmf.ModifyPortalContent" par exemple.
- Créez un package content avec une classe MyContent avec le stéréotype archetypes.
- Créez une dépendance de MyView vers MyContent.

Vous aurez accès à la vue @@myview seulement si le context est un document MyContent et que vous avez la permission cmf.ModifyPortalContent.

Exercice
========
Mise en pratique sur le composant « base de connaissances »
