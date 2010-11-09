# -*- coding: utf-8 -*-
# $Id$
"""Packaging and setup for formation.portlet.author"""

from setuptools import setup, find_packages
import os

version = '1.0.0'

def read(*names):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, *names)
    return open(path, 'r').read().strip()

version = read('formation', 'portlet', 'author', 'version.txt')

setup(name='formation.portlet.author',
      version=version,
      description="Shows the context author summary in a portlet",
      long_description=read("README.txt") + "\n" +
                       read("docs", "HISTORY.txt"),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Programming Language :: Python",
          "Operating System :: OS Independent"
        ],
      keywords='plone portlet author',
      author='Gilles Lenfant',
      author_email='gilles.lenfant@gmail.com',
      url='https://svn.plone.org/svn/collective/collective.trainingmanual/trunk/fr/examples/formation.portlet.author',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['formation', 'formation.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
