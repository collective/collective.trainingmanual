================================
L'environnement de développement
================================

Le but est de présenter et permettre l'acquisition des outils utilisés pour le développement Plone 3.

Installation de Python 2.4
==========================
Sur Ubuntu : ::

    apt-get install python2.4 python2.4-dev build-essential libxml2-dev libxslt1-dev libjpeg62-dev zlib1g-dev libfreetype6-dev

build-essential permet d'installer le compilateur gcc et make entre autres.

Configuration de l'éditeur vim
==============================
Installez gvim : ::

    apt-get install vim-gnome

Créez un fichier *~/.vimrc* avec la configuration suivante : ::

    " http://www.vex.net/~x/python_and_vim.html
    " for Python
    ab pdbs import pdb; pdb.set_trace ()
    " (Ne mettez pas l'espace avant les parenthèses)
    set pastetoggle=<F8>
    syntax on
    autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class tabstop=4 shiftwidth=4 smarttab expandtab softtabstop=4
    autocmd BufRead *.xml,*pt set smartindent tabstop=2 shiftwidth=2 smarttab expandtab softtabstop=2
    autocmd BufRead *.rst set smartindent tabstop=4 shiftwidth=4 smarttab expandtab softtabstop=4

Cette configuration permet de configurer l'indentation à 4 espaces pour les fichiers Python et reST, 2 espaces pour les fichiers XML et PT. Elle permet aussi d'activer la coloration syntaxique et passer en mode "collage" à l'aide de la touche F8.

Configuration de l'autocomplétion dans Python
=============================================
Créer un fichier *~/.pythonstartup* avec le contenu suivant : ::

    # python startup file
    import readline
    import rlcompleter
    import atexit
    import os
    # tab completion
    readline.parse_and_bind('tab: complete')
    # history file
    histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)
    del os, histfile, readline, rlcompleter

Éditez *~/.bashrc* et décommentez les 3 lignes qui incluent *~/.bash_aliases*.

Créez le fichier *~/.bash_aliases* avec le contenu : ::

    export PYTHONSTARTUP=~/.pythonstartup

    alias archgenxml=~/workspace/archgenxml_buildout/bin/archgenxml
    alias argouml="cd ~/opt/argouml-0.28/ && ./argouml.sh"
    export EDITOR=vim

    # https://wiki.ubuntu.com/Spec/EnhancedBash
    shopt -s histappend
    PROMPT_COMMAND="history -a; $PROMPT_COMMAND"
    export HISTSIZE=1000
    export HISTFILESIZE=1000
    export GREP_OPTIONS='--color=auto --exclude=*.svn-base --exclude=*.pyc'

Ici nous avons en plus les alias pour archgenxml et argouml que vous installerez par la suite.
La dernière section est pour partager l'historique à travers tous les terminaux et mettre de la couleur pour la commande grep.


Activation de la recherche dans l'historique
============================================
Dans le fichier */etc/inputrc* décommenter ces lignes : ::

    "\e[5~": history-search-backward
    "\e[6~": history-search-forward

Ces lignes permettent de rechercher dans l'historique de bash avec les touches Page Up/Page Down.
Par exemple, tapez ``ssh<PageUp>``.

Installation de ArgoUML et ArchGenXML
=====================================
Suivre la `documentation de ArchGenXML`_.

Pour vite installer ArgoUML::

    sudo apt-get install sun-java6-jdk
    mkdir ~/opt
    mkdir ~/downloads
    cd ~/downloads
    wget http://argouml-downloads.tigris.org/nonav/argouml-0.28.1/ArgoUML-0.28.1.tar.gz
    cd ~/opt
    tar xvf /home/vincentfretin/downloads/ArgoUML-0.28.1.tar.gzmkdir ~/opt

.. _`documentation de ArchGenXML`: http://plone.org/documentation/manual/archgenxml2/startup/installation


Checkout svn.zope.org
=====================
Si vous avez un accès subversion au dépôt de Zope, créez votre fichier *~/.ssh/config* comme ceci::

    Host svn.zope.org
    User votre_login

Comme cela, si votre compte unix est différent de votre compte svn, vous n'aurez pas besoin de spécifier votre login lors d'un checkout.

Pour réaliser un checkout::

    svn co svn+ssh://svn.zope.org/repos/main/grok

