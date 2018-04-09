# -*- coding: utf-8 -*-
#
#   This file is part of Candyshop
#   Copyright (C) 2016, Candyshop Developers
#   All rights reserved.
#
#   Please refer to AUTHORS.md for a complete list of Copyright
#   holders.
#
#   Candyshop is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Candyshop is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
``candyshop.environment`` is a module for creating Odoo environments.

This module implements an abstraction layer to create an environment where
bundles can be consulted for different reports.
"""

import os
import sys
import shutil
import tempfile

from sh import git

from .bundle import Bundle

DEFAULT_URL = 'https://github.com/odoo/odoo'
DEFAULT_BRANCH = '8.0'


class Environment(object):
    """
    An Environment is a virtual space where you can enclose bundles.

    Think about it as an invisible container where you can put bundles
    to study its relationships; for example, listing all modules and see which
    ones have missing dependencies (that are not within the environment).
    """

    def __init__(self, init=True, init_from=None,
                 url=DEFAULT_URL, branch=DEFAULT_BRANCH):
        """
        Initialize the ``Environment`` instance.

        :param init: (boolean) specifies if the environment should be
                     initialized, that is, if an Odoo repo should be cloned
                     and the native addons added as bundles. Default: True.
        :param init_from: (string) a path pointing to an Odoo codebase. If
                          present, the Odoo codebase will be taken from this
                          folder instead of cloning from start.
        :param url: (string) an URL pointing to a git repository. This URL is
                     used to clone the Odoo Codebase if ``init`` is ``True``
                     and ``init_from`` is ``None``.
        :param branch: (string) the branch used to clone ``url``.
        :return: an ``Environment`` instance.

        .. versionadded:: 0.1.0
        """
        #: Attribute ``Environment.bundles`` (list): A list of ``Bundle``
        #: instances representing the bundles contained in this environment.
        self.bundles = []

        #: Attribute ``Environment.path`` (string): A path pointing to
        #: the temporary directory where odoo and OCA dependencies will be
        #: cloned.
        self.path = tempfile.mkdtemp()

        if init:
            self.__initialize_odoo(url, branch, init_from)

    def __initialize_odoo(self, url=DEFAULT_URL, branch=DEFAULT_BRANCH,
                          init_from=None):
        """
        Private method to clone an Odoo codebase inside the Environment path.

        This method clones an odoo codebase specified by ``url`` and
        ``branch`` so that bundles can have the native odoo bundles to compare
        with. Without this method, native modules (base, board, etc) would
        appear as missing dependencies.

        .. versionadded:: 0.1.0
        """
        if init_from:
            odoo_dir = os.path.abspath(init_from)
        else:
            odoo_dir = os.path.join(self.path, 'odoo')
            if not os.path.isdir(odoo_dir):
                self.__git_clone(url, branch, odoo_dir)
        self.addbundles([
            os.path.join(odoo_dir, 'addons'),
            os.path.join(odoo_dir, 'openerp', 'addons')
        ])

    @staticmethod
    def __git_clone(url, branch, path):
        """
        Private method to clone a git repository.

        This method clones a git repository specified by ``url`` and
        ``branch`` to a folder ``path``. The ``--depth=1`` option is passed
        to the command to avoid cloning full history.

        .. versionadded:: 0.1.0
        """
        try:
            git.clone(url, path, quiet=True, depth=1, branch=branch)
        except BaseException:
            print('There was a problem cloning {0}.'.format(url))
            raise

    def __clone_deptree(self):
        """
        Private method that clones the dependency tree of existing bundles.

        It reads the oca_dependencies attribute of each bundle, clones each one
        (if any) and then adds them as bundles (which invokes this method again
        to satisfy dependencies in the new bundles).

        .. versionadded:: 0.1.0
        """
        for bundle in self.bundles:
            for name, url, branch in bundle.oca_dependencies:
                bundle_dir = os.path.join(self.path, name)
                if os.path.isdir(bundle_dir):
                    continue
                self.__git_clone(url=url, branch=branch, path=bundle_dir)
                self.addbundles([bundle_dir])

    def __deps_notin_e(self, deps=None):
        """
        Private method that informs about missing modules in the environment.

        :param deps: (list) a list of module names to check.
        :return: (generator) a generator that produces an iterable of
                 module names that are not present in the environment.

        .. versionadded:: 0.1.0
        """
        deps = deps or []
        for dep in deps:
            if dep not in self.get_modules_slug_list():
                yield dep

    def addbundles(self, locations=None, exclude_tests=True):
        """
        Public method that inserts bundles inside the environment.

        This method register a list of bundles and builds the dependency tree
        of each bundle recursively by calling ``__clone_deptree()``.

        :param locations: (list) a list of strings containing relative or
                          absolute paths to directories containig bundles.
        :param exclude_tests: (boolean) if ``True``, will exclude modules
                              inside ``tests`` directories.

        .. versionadded:: 0.1.0
        """
        locations = locations or []
        for location in locations:
            location = os.path.abspath(location)
            if location in self.get_bundle_path_list():
                continue
            try:
                self.bundles.append(Bundle(location, exclude_tests))
            except BaseException:
                print(('There was a problem inserting the bundle'
                       ' located at {0}').format(location))
                raise
            else:
                self.__clone_deptree()

    def destroy(self):
        """
        Public method to destroy an ``Environment`` instance.

        This method empties the bundle list and deletes the environment path,
        including all previously clones bundles.

        .. versionadded:: 0.1.0
        """
        self.bundles = []
        shutil.rmtree(self.path)

    def reset(self):
        """
        Public method to destroy and initialize the ``Environment`` instance.

        This method calls ``self.destroy()`` on the instance and then
        re-initializes the Odoo environment.
        """
        self.destroy()
        self.__initialize_odoo()

    def get_bundle_path_list(self):
        """
        Public method that informs about bundle paths.

        :return: (generator) a generator that produces an iterable of
                 paths pointing to the bundles registered so far.

        .. versionadded:: 0.1.0
        """
        for bundle in self.bundles:
            yield bundle.path

    def get_modules_list(self):
        """
        Public method that informs about modules instances.

        :return: (generator) a generator that produces an iterable of
                 ``Module`` instances of all the modules present within
                 the environment.

        .. versionadded:: 0.1.0
        """
        for bundle in self.bundles:
            for module in bundle.modules:
                yield module

    def get_modules_slug_list(self):
        """
        Public method that informs about module names.

        :return: (generator) a generator that produces an iterable of strings
                 containing the names of all the modules present within the
                 environment.

        .. versionadded:: 0.1.0
        """
        for bundle in self.bundles:
            for module in bundle.modules:
                yield module.properties.slug

    def get_notmet_dependencies(self):
        """
        Public method that informs about missing dependencies in modules.

        :return: (generator) a generator that produces an iterable of
                 dictionaries containing references to each bundle that have
                 unmet dependencies within a module. The output is something
                 similar tho this::

                    [
                        {'bundle-name': {
                            'module_name': ['missing_module_a',
                                            'missing_module_b']
                            }
                        }
                    ]

        .. versionadded:: 0.1.0
        """
        for module in self.get_modules_list():
            if hasattr(module.properties, 'depends'):
                deplist = list(self.__deps_notin_e(module.properties.depends))
                if not deplist:
                    continue
                yield {module.bundle.name: {module.properties.slug: deplist}}

    def get_notmet_record_ids(self):
        """
        Public method that informs about missing dependencies in XML files.

        :return: (generator) a generator that produces an iterable of
                 dictionaries containing references to each bundle that have
                 unmet dependencies refereced inside XML record ids. The output
                 is something similar to this::

                    [
                        {'bundle-name': {
                            'module_name/path/file.xml': ['missing_module_a',
                                                          'missing_module_b']
                             }
                        }
                    ]

        .. versionadded:: 0.1.0
        """
        for module in self.get_modules_list():
            for data in module.get_record_ids_module_references():
                for xml, refs in data.items():
                    deplist = list(self.__deps_notin_e(refs))
                    if not deplist:
                        continue
                    relxml = os.path.join(module.properties.slug, xml)
                    yield {module.bundle.name: {relxml: deplist}}

    def get_notmet_dependencies_report(self):
        """
        Public method that reports missing dependencies in modules.

        :return: (string) a report of human readable output for the
                 ``get_notmet_dependencies()`` method.

        .. versionadded:: 0.1.0
        """
        report = list(self.get_notmet_dependencies())
        if report:
            print('The following module dependencies are not found'
                  ' in the environment:')
            for item in report:
                bundle, data = list(item.items())[0]
                module, depends = list(data.items())[0]
                print('')
                print('    Bundle: {0}'.format(bundle))
                print('    Module: {0}'.format(module))
                print('    Missing dependencies:')
                for dep in depends:
                    print('        - {0}'.format(dep))
            print('')
            sys.exit(1)
        else:
            print('All dependencies are satisfied in the environment.')

    def get_notmet_record_ids_report(self):
        """
        Public method that reports missing dependencies in XML files.

        :return: (string) a report of human readable output for the
                 ``get_notmet_record_ids()`` method.

        .. versionadded:: 0.1.0
        """
        report = list(self.get_notmet_record_ids())
        if report:
            print('The following record ids are not found in the environment:')
            for item in report:
                bundle, data = list(item.items())[0]
                xmlfile, depends = list(data.items())[0]
                print('')
                print('    Bundle: {0}'.format(bundle))
                print('    XML file: {0}'.format(xmlfile))
                print('    Missing references:')
                for dep in depends:
                    print('        - {0}'.format(dep))
            print('')
            sys.exit(1)
        else:
            print('All references are present in the environment.')
