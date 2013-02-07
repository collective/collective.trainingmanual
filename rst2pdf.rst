====================================
Installation de ReportLab et rst2pdf
====================================

Sous Ubuntu 8.04, vous pouvez installer la package python-reportlab,
qui est la version 2.3. Cependant cette version a un bogue sur le
deepcopy (reportlab/platypus/flowables.py:448) qui empêche rst2pdf
de fonctionner. La version 2.2 fonctionne.


Installation de ReportLab
=========================

Installez ReportLab comme ceci : ::

    wget http://www.reportlab.org/ftp/ReportLab_2_2.tgz
    tar xvf ReportLab_2_2.tgz
    cd ReportLab_2_2/
    python2.4 setup.py build
    sudo python2.4 setup.py install


Installation de rst2pdf
=======================

Dans un virtualenv, installez PIL (pour la génération des images) et rst2pdf comme ceci : ::

    mkvirtualenv -p /usr/bin/python2.4 rst2pdf
    easy_install -f http://dist.plone.org/thirdparty PIL
    easy_install -b. -e rst2pdf
    cd rst2pdf/

Commentez la dépendance reportlab dans setup.py and installez rst2pdf comme ceci : ::

    python setup.py install


Utilisation
===========

Un exemple d'utilisation de rst2pdf : ::

    rst2pdf -o index.pdf index.rst

