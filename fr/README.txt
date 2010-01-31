Tout d'abord installez ce qu'il faut :
apt-get install tetex-base tetex-bin tetex-extra
mkvirtualenv sphinx
easy_install sphinx

récupérez les sources :
svn co https://svn.plone.org/svn/collective/collective.trainingmanual/trunk/fr collective.trainingmanual
cd collective.trainingmanual/sphinx

pour la version html :
make html
firefox build/html/index.html

pour la version pdf :
make latex
cd build/latex
make all-pdf
evince FormationPlone.pdf
