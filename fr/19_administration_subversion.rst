=====================================
Administration d'un dépôt subversions
=====================================

Faire un dump d'un dépôt existant
=================================
Exécutez : ::
    
    svnadmin dump /home/svn/Agile > /tmp/svn_agile.dump

Importer les révisions dans un autre dépôt
==========================================
Commandes : ::

    svnadmin create /home/svn/autre
    svnadmin load /home/svn/autre < /tmp/svn_agile.dump

On vérifie : ::

    svn co file:///home/svn/autre
