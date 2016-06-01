#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements
from pip.download import PipSession

from candyshop import (__author__, __email__, __version__,__url__,
                       __description__)

def cat(f):
    with open(f) as o:
        return o.read()

def reqs(r):
    for req in parse_requirements(r, session= PipSession()):
        yield str(req.req)

setup(
    name='candyshop',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    description=__description__,
    long_description='%s\n\n%s' % (cat('README.rst'), cat('HISTORY.rst')),
    packages=[
        'candyshop',
    ],
    package_dir={'candyshop':
                 'candyshop'},
    include_package_data=True,
    install_requires=list(reqs('requirements.txt')),
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
    tests_require=list(reqs('requirements_dev.txt'))
)
