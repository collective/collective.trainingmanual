===================================
Programmation dirigée par les tests
===================================

Définition
==========
Apprentissage des techniques qui permettent d'assurer la qualité du logiciel.
Apprendre à écrire des tests unitaires, d'intégration et fonctionnels.

Savoir
======
- Tests unitaires avec le module unittest
- Tests d'intégration
- Tests fonctionnels avec selenium IDE

Test unitaire
=============
Les tests unitaires sont écrit à l'aide du module unittest.

Dans un packages Python, la convention est de créer soit un module tests.py, soit un package tests avec plusieurs fichiers commencant par *test_* dans ce packages. Il est en général conseillé de commencer tout de suite avec un package tests, plutôt qu'un module si l'on sait que le projet contiendra de nombreux modules. En effet la convention est de créer un fichier test_${module}.py pour chacun des modules de votre application.

Donc dans votre package, créez un packages tests : ::

  mkdir tests
  touch tests/__init__.py

Lancer les tests ::

    bin/instance test -s collective.groupdelegation

Vous pouvez utiliser la recipe zc.recipe.testrunner pour créer un script ``bin/test`` qui teste plusieurs eggs : ::

    [test]
    recipe = zc.recipe.testrunner
    eggs =
        collective.groupdelegation
        formation.portlet.docinfo


Exercice
========
Écriture des différents types de tests sur le composant « base de connaissances »
