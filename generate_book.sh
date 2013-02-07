#!/bin/bash

cd ~/sphinx
. bin/activate
cd collective.trainingmanual
svn up > /dev/null
cd integrateur

make clean > /dev/null
make html > /dev/null 2>&1
if [ $? == 0 ]; then
  rm -rf ~/html/integrateur
  cp -rf ~/sphinx/collective.trainingmanual/integrateur/build/html/ ~/html/integrateur
else
  echo "integrateur html generation failed"
fi


make latex > /dev/null 2>&1
if [ $? == 0 ]; then
  cd build/latex
  make all-pdf > /dev/null 2>&1
  if [ $? == 0 ]; then
    cp ~/sphinx/collective.trainingmanual/integrateur/build/latex/FormationPloneIntegrateur.pdf ~/html/integrateur/
  else
    echo "integrateur pdf generation failed"
  fi
else
  echo "integrateur latex generation failed"
fi



cd ~/sphinx/collective.trainingmanual/developpeur

make clean > /dev/null
make html > /dev/null 2>&1
if [ $? == 0 ]; then
  rm -rf ~/html/developpeur
  cp -rf ~/sphinx/collective.trainingmanual/developpeur/build/html/ ~/html/developpeur
else
  echo "developpeur html generation failed"
fi


make latex > /dev/null 2>&1
if [ $? == 0 ]; then
  cd build/latex
  make all-pdf > /dev/null 2>&1
  if [ $? == 0 ]; then
    cp ~/sphinx/collective.trainingmanual/developpeur/build/latex/FormationPloneDeveloppeur.pdf ~/html/developpeur/
  else
    echo "developpeur pdf generation failed"
  fi
else
  echo "developpeur latex generation failed"
fi
