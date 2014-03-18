# -*- coding: utf-8 -*-
"""Installer for the imio.dms.ws package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='imio.dms.ws',
    version='0.1',
    description="Dms webservice integration with json format",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='',
    author='Stephan Geulette (IMIO)',
    author_email='s.geulette@imio.be',
    url='http://pypi.python.org/pypi/imio.dms.ws',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['imio', 'imio.dms'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.jsonapi.core',
        'five.grok',
        'plone.api',
        'setuptools',
        'jsonschema',
        'z3c.json',
        'Products.CPUtils',
        'python-cjson',
    ],
    extras_require={
        'test': [
            'ecreall.helpers.testing',
            'plone.app.testing',
            'plone.app.robotframework',
            'ipdb',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    ws_test = imio.dms.ws.client:ws_test
    """,
)
