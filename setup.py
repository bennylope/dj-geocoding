#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import dj_geocoding

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = dj_geocoding.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='dj-geocoding',
    version=version,
    description="""Django integration for geocoding (using Geocodio)""",
    long_description=readme + '\n\n' + history,
    author='Ben Lopatin',
    author_email='ben@wellfire.co',
    url='https://github.com/bennylope/dj-geocoding',
    packages=[
        'dj_geocoding',
    ],
    include_package_data=True,
    install_requires=[
        'pygeocodio>=0.3.0'
    ],
    license="BSD",
    zip_safe=False,
    keywords='dj-geocoding',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
