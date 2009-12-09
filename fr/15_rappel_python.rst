=================
Rappel sur Python
=================

Définition
==========
Le but est de maîtriser le langage python, de comprendre et respecter les standards utilisés par la communauté Plone. 

Savoir
======
- Installation de python
- Votre premier programme Python
- Types prédéfinis
- Le pouvoir de l’introspection
- Les objets et l'orienté objet
- Traitement des exceptions et utilisation de fichiers
- Expressions régulières
- Traitement du HTML
- Traitement de données XML
- Des scripts et des flots de données (streams)

Attributs par défaut d'une classe
=================================
Dans un shell Python : ::

    >>> class MyClass(object):
    ...     myattr = 2
    ... 
    >>> a = MyClass()
    >>> a.myattr
    2
    >>> a.__dict__
    {}
    >>> a.myattr = 3
    >>> a.myattr
    3
    >>> a.__dict__
    {'myattr': 3}
    >>> b = MyClass()
    >>> b.myattr
    2
    >>> MyClass.myattr = 4
    >>> b.myattr
    4
    >>> a.myattr
    3

set
===
C'est une liste à élément unique : ::

    >>> s set([1,2,3,1,5])
    >>> s = set([1,2,3,1,5])
    >>> s
    set([1, 2, 3, 5])
    >>> s.add(6)
    >>> s
    set([1, 2, 3, 5, 6])
    >>> s2 = frozenset([1,2])
    >>> s2.add(3)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'frozenset' object has no attribute 'add'
    >>>

Le __call__ d'une classe
========================
Une classe peut être appelé : ::

    >>> class A(object):
    ...   def __call__(self):
    ...     print "bonjour"
    ... 
    >>> a = A()
    >>> a()
    bonjour

Manipulation de chaines
=======================
::

    >>> "bonJour".capitalize()
    'Bonjour'
    >>> "bonjour"[0]
    'b'
    >>> "bonjour"[-1]
    'r'
    >>> "bonjour"[0:3]
    'bon'
    >>> "bonjour"[:3]
    'bon'
    >>> "bonjour"[1:3]
    'on'
    >>> "bonjour"[-2:-1]
    'u'
    >>> "bonjour"[-2:]
    'ur'
    >>> "bonjour"[1:5:2]
    'oj'

Différence entre unicode et string
==================================
- http://www.stereoplex.com/two-voices/python-unicode-and-unicodedecodeerror

Comprehensive list et generator
===============================
::

    >>> [i*2 for i in range(10)]
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    >>> (i*2 for i in range(10))
    <generator object at 0x1745ef0>
    >>> g = (i*2 for i in range(10))
    >>> g.next()
    0
    >>> g.next()
    2
    >>> g.next()
    4
    >>> g.next()
    6
    >>> g.next()
    8
    >>> for i in g:
    ...   print i
    ... 
    10
    12
    14
    16
    18
    >>> g.next()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    StopIteration

Methode de classe
=================
::

    >>> class A(object):
    ...   @classmethod
    ...   def m(cls):
    ...     print "classmethod"
    ...   def n(self):
    ...     print "dans n"
    ... 
    >>> a = A()
    >>> a.n()
    dans n
    >>> A.m()
    classmethod
    >>> a.m()
    classmethod
    >>> A.n()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unbound method n() must be called with A instance as first argument (got nothing instead)

Property
========
Exemple : ::

    >>> class A(object):
    ...   myattr = 3
    ... 
    >>> a = A()
    >>> a.myattr = 5
    >>> a.myattr
    5
    >>> class A(object):
    ...   def setMyAttr(self, value):
    ...     self._myattr = value * 2
    ...   def getMyAttr(self):
    ...     return self._myattr
    ...   myattr = property(getMyAttr, setMyAttr)
    ... 
    >>> b = A()
    >>> b.myattr = 3
    >>> b.myattr
    6

Debogueur pdb
=============
À insérer dans le code source à l'endroit où vous voulez vous arrêter : ::

    import pdb; pdb.set_trace ()

(Ne mettez pas l'espace avant les parenthèses)

À partir de là, vous avez les commandes suivantes :

- s/step : entre dans la fonction
- n/next : instruction suivante
- c/continue : continuer jusqu'au prochain point d'arrêt
- l/list : affiche le contexte
- u/up : monter dans la pile d'appel
- d/down : descendre dans la pile d'appel
- break num_line : ajouter un point d'arrêt à la ligne num_line
- a : affiche la liste des paramètres passés à la fonction

Profiler
========
Installez le package Ubuntu pour avoir les modules profile et pstats : ::

    $ sudo apt-get install python-profiler

Dans votre code, pour obtenir des statistiques sur l'appel de la methode : ::

    self.method(arg1, arg2)

remplacez la ligne par : ::

    import profile
    p = profile.Profile()
    p.runcall(self.method, arg1, arg2)
    p.dump_stats('/tmp/stats')

Les résultats seront sauvegardés dans le fichier */tmp/stats*.

Pour ensuite afficher les résultats, ouvrez un Python shell et exécutez : ::

    import pstats
    p = pstats.Stats('/tmp/stats')
    p.strip_dirs().sort_stats(-1).print_stats()

`Plus d'informations sur le module profile. <http://docs.python.org/library/profile.html>`__

Ressources
==========
- livre `Plongez au coeur de Python`_

.. _`Plongez au coeur de Python`: http://diveintopython.adrahon.org/

Exercice
========
Lecture d'un fichier, traitement avec une expression régulière et écriture des résultats dans un fichier.
