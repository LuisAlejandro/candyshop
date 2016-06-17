#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from candyshop import (__author__, __email__, __version__,__url__,
                       __description__)

setup(
    name='candyshop',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    description=__description__,
    long_description='{0}\n\n{1}'.format(open('README.rst').read(),
                                         open('HISTORY.rst').read()),
    packages=[
        'candyshop',
    ],
    package_dir={'candyshop':
                 'candyshop'},
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    license='AGPL-3',
    zip_safe=False,
    keywords='candyshop',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=open('requirements-dev.txt').read().split('\n')
)
