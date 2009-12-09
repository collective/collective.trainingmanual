======================================
Présentation des nouveautés de Plone 3
======================================

Présentation des nouveautés de Plone 3 par rapport à la version Plone 2.5.

Édition en ligne
================
`Description de la fonctionnalité "Inline editing" <http://plone.org/products/plone/features/3.0/new/inline-editing>`__

Désactivé par défaut dans Plone 3.3. Pour l'activer, cochez "Activer l'édition en ligne" dans "Configuration du site -> Site"

Validation des champs via AJAX
==============================
La validation d'un champ d'un formulaire se fait dès que vous le quittez.

Support des copies de travail
=============================
`Working Copy support <http://plone.org/products/plone/features/3.0/new/working-copy-support>`__

Installez le produit "Working Copy Support (Iterate)" via "Configuration du site -> Produits d'extension".

Vous avez maintenant une nouvelle action "Créer un brouillon" accessible sur n'importe quel contenu.

Vérification de l'intégrité des liens
=====================================
`Link and reference integrity checking <http://plone.org/products/plone/features/3.0/new/link-and-reference-integrity-checking>`__

Lors de la suppression d'une image, Plone regarde si des documents sont en train de l'utiliser pour éviter de casser des liens.

Verrouillage d'un document lors de l'édition
============================================
`Automatic locking and unlocking <http://plone.org/products/plone/features/3.0/new/automatic-locking-and-unlocking>`__

Le document est verrouillé lorsque vous l'éditez. Cela permet d'éviter à un autre utilisateur d'éditer en même temps et d'écraser votre travail.

Le verrouillage a été amélioré dans Plone 3.3. Le verrouillage n'est actif que 10 minutes, reconductible si l'utilisateur est toujours en train de l'éditer.

Nouvel onglet partage
=====================
`Easy collaboration and sharing <http://plone.org/products/plone/features/3.0/new/easy-collaboration-and-sharing>`__

L'onglet partage a été amélioré, plus simple d'utilisation.
Chaque intitulé des colonnes correspond à un rôle.

- *Peut Ajouter* : Contributor
- *Peut modifier* : Editor
- *Peut voir* : Reader
- *Peut Modérer* : Reviewer

Versionnement des documents
===========================
`Versioning, history and reverting content <http://plone.org/products/plone/features/3.0/new/versioning-history-and-reverting-content>`__

Vous pouvez activer le versionnement d'un type de contenu à partir de "Configuration du site -> Types".

Pour pouvoir visualiser les différences entre deux versions, il faut ajouter le type de contenu dans portal_diff.

Visualiser un document en mode diaporama
========================================
`Presentation mode for content <http://plone.org/products/plone/features/3.0/new/presentation-mode-for-content>`__

Éditez le document et allez dans Paramètres pour cocher "Mode présentation".

Navigation Précédent/Suivant dans un dossier
============================================
`Automatic previous/next navigation <http://plone.org/products/plone/features/3.0/new/automatic-previous-next-navigation>`__

À partir d'un document d'un dossier, vous avez la possibilité d'ouvrir le document précédent ou le suivant.

Éditez le dossier et allez dans Paramètres pour cocher "Activer la navigation 'précédent/suivant'".


Générer une table des matières pour un document
===============================================
`Auto-generated tables of contents <http://plone.org/products/plone/features/3.0/new/always-updated-table-of-contents>`__

Éditez le document et allez dans Paramètres pour cocher "Table des matières".

Indexage des documents Word et PDF
==================================
`Full-text indexing of Word and PDF documents <http://plone.org/products/plone/features/3.0/new/full-text-indexing-of-word-and-pdf-documents>`__

Plone indexe le texte des documents Word et PDF. Il est donc ensuite possible de rechercher un terme qui est dans ces documents.
Cette fonctionnalité est active si vous avez les packages Ubuntu *wv* (pour les documents Word) et *poppler-utils* (pour la commande pdftotext) d'installés. `Voir howto <http://plone.org/documentation/how-to/enable-full-text-indexing-of-word-documents-and-pdfs-in-plone-3-0-gnu-linux/>`__

D'autres formats peuvent être indexés avec le produit `ARFilePreview`_, qui nécessite `AROfficeTransforms`_ ou le nouveau `plone.transforms`_.

- `ARFilePreview-v2 branch (2.3.0)`_ fonctionne avec `AROfficeTransforms`_ (utilise portal_transforms).
- `ARFilePreview trunk v3`_ fonctionne avec `plone.transforms`_ (architecture Zope 3).


.. _`ARFilePreview`: http://plone.org/products/arfilepreview/
.. _`AROfficeTransforms`: http://plone.org/products/arofficetransforms/
.. _`plone.transforms`: http://pypi.python.org/pypi/plone.transforms
.. _`ARFilePreview-v2 branch (2.3.0)`: http://svn.plone.org/svn/collective/ARFilePreview/branches/ARFilePreview-v2
.. _`ARFilePreview trunk v3`: http://svn.plone.org/svn/collective/ARFilePreview/trunk

Mais aussi
==========
- Upgraded visual HTML editor
- Powerful workflow capabilities
- Flexible authentication back-end
- Collections
- Support for the search engine Sitemap protocol
- Support for multiple mark-up formats
- Wiki support
- Rules engine for content
- Portlets engine

En savoir plus : `Features in Plone 3`_

.. _`Features in Plone 3`: http://plone.org/products/plone/features/3.0


Et pour le développeur
======================
Technologies qui ont fait leur entrée dans Plone 2.5 et qui sont maintenant incontournable dans Plone 3 :

- profils GenericSetup pour importer/exporter une configuration de site
- technologies Zope 3 (évènements, vues...)

