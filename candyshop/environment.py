#   -*- coding: utf-8 -*-
#   This file is part of Odoo Candyshop
#   ------------------------------------------------------------------------
#   Copyright:
#   Copyright (c) 2016, Vauxoo (<http://vauxoo.com>)
#   All Rights Reserved
#   ------------------------------------------------------------------------
#   Contributors:
#   Author: Luis Alejandro Martínez Faneyth (luisalejandro@vauxoo.com)
#   ------------------------------------------------------------------------
#   License:
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#   ------------------------------------------------------------------------
'''
candyshop.environment module
----------------------------

This module implements an abstraction layer to create an environment where
bundles can be consulted for different reports.
'''

import os
import sys
import tempfile

from sh import git

from .bundle import Bundle

DEFAULT_REPO = 'https://github.com/vauxoo/odoo'
DEFAULT_BRANCH = '8.0'


class OdooEnvironment(object):
    '''
    .. versionadded:: 0.1.0

    An Odoo Environment is a virtual environment where you can enclose Odoo
    bundles. Think about it as an invisible container where you can put bundles
    to study its relationships; for example, listing all modules and see which
    ones have missing dependencies (that are not within the environment).

    :param init: (boolean) specifies if the environment should be initialized,
                 that is, if an Odoo repo should be cloned and the native
                 addons added as bundles. Default: True.
    :param init_from: (string) a path pointing to an Odoo codebase. If present,
                      the Odoo codebase will be taken from this folder instead
                      of cloning from start.
    :param repo: (string) a URI pointing to a git repository. This URI is used
                 to clone the Odoo Codebase if ``init`` is ``True`` and
                 ``init_from`` is ``None``.
    :param branch: (string) the branch used to clone ``repo``.
    :return: an ``OdooEnvironment`` instance.
    '''
    def __init__(self, init=True, init_from=None,
                 repo=DEFAULT_REPO, branch=DEFAULT_BRANCH):

        #: Attribute ``OdooEnvironment.bundles`` (list): A list of ``Bundle``
        #: instances representing the bundles contained in this environment.
        self.bundles = []

        #: Attribute ``OdooEnvironment.path`` (string): A path pointing to
        #: the temporary directory where odoo and OCA dependencies will be
        #: cloned.
        self.path = tempfile.mkdtemp()

        if init:
            self.__initialize_odoo(repo, branch, init_from)

    def __initialize_odoo(self, repo=DEFAULT_REPO, branch=DEFAULT_BRANCH,
                          init_from=None):
        '''
        .. versionadded:: 0.1.0

        Private method to clone an Odoo codebase to the Environment path.
        '''
        if init_from:
            odoo_dir = os.path.abspath(init_from)
        else:
            odoo_dir = os.path.join(self.path, 'odoo')
            if not os.path.isdir(odoo_dir):
                self.git_clone(repo, branch, odoo_dir)
        self.addbundles([
            os.path.join(odoo_dir, 'addons'),
            os.path.join(odoo_dir, 'openerp', 'addons')
        ])

    def __git_clone(self, repo, branch, path):
        '''
        .. versionadded:: 0.1.0


        '''
        try:
            git.clone(repo, path, quiet=True, depth=1, branch=branch)
        except BaseException:
            print('There was a problem cloning %s.' % repo)
            raise

    def __satisfy_oca_dependencies(self):
        '''
        .. versionadded:: 0.1.0


        '''
        for bundle in self.bundles:
            for name, repo in bundle.oca_dependencies.items():
                bundle_dir = os.path.join(self.path, name)
                if not os.path.isdir(bundle_dir):
                    self.__git_clone(repo=repo, branch=DEFAULT_BRANCH,
                                     path=bundle_dir)
                    self.addbundles([bundle_dir])
                    self.__satisfy_oca_dependencies()

    def addbundles(self, locations=[], exclude_tests=True):
        '''
        .. versionadded:: 0.1.0


        '''
        for location in locations:
            location = os.path.abspath(location)
            if location not in self.get_bundle_path_list():
                try:
                    self.bundles.append(Bundle(location, exclude_tests))
                except BaseException:
                    print(('There was a problem inserting the bundle'
                           ' located at %s') % location)
                    raise
                else:
                    self.__satisfy_oca_dependencies()

    def get_bundle_path_list(self):
        '''
        .. versionadded:: 0.1.0


        '''
        for bundle in self.bundles:
            yield bundle.path

    def get_modules_list(self):
        '''
        .. versionadded:: 0.1.0


        '''
        for bundle in self.bundles:
            for module in bundle.modules:
                yield module

    def get_modules_slug_list(self):
        '''
        .. versionadded:: 0.1.0


        '''
        for bundle in self.bundles:
            for module in bundle.modules:
                yield module.properties.slug

    def __deps_notin_e(self, deps):
        '''
        .. versionadded:: 0.1.0


        '''
        for dep in deps:
            if dep not in self.get_modules_slug_list():
                yield dep

    def get_notmet_dependencies(self):
        '''
        .. versionadded:: 0.1.0


        '''
        for module in self.get_modules_list():
            if hasattr(module.properties, 'depends'):
                deplist = list(self.__deps_notin_e(module.properties.depends))
                if deplist:
                    yield {module.bundle.name:
                           {module.properties.slug: deplist}}

    def get_notmet_record_ids(self):
        '''
        .. versionadded:: 0.1.0


        '''
        for module in self.get_modules_list():
            for data in module.get_record_ids_module_references():
                for xml, refs in data.items():
                    deplist = list(self.__deps_notin_e(refs))
                    if deplist:
                        relxml = os.path.join(module.properties.slug, xml)
                        yield {module.bundle.name: {relxml: deplist}}

    def get_notmet_dependencies_report(self):
        '''
        .. versionadded:: 0.1.0


        '''
        report = list(self.get_notmet_dependencies())
        if report:
            print('The following module dependencies are not found'
                  ' in the environment:')
            for item in report:
                bundle, data = list(item.items())[0]
                module, depends = list(data.items())[0]
                print('')
                print('    Bundle: %s' % bundle)
                print('    Module: %s' % module)
                print('    Missing dependencies:')
                for dep in depends:
                    print('        - %s' % dep)
            print('')
            sys.exit(1)
        else:
            print('All dependencies are satisfied in the environment.')

    def get_notmet_record_ids_report(self):
        '''
        .. versionadded:: 0.1.0


        '''
        report = list(self.get_notmet_record_ids())
        if report:
            print('The following record ids are not found in the environment:')
            for item in report:
                bundle, data = item.items()[0]
                xmlfile, depends = data.items()[0]
                print('')
                print('    Bundle: %s' % bundle)
                print('    XML file: %s' % xmlfile)
                print('    Missing references:')
                for dep in depends:
                    print('        - %s' % dep)
            print('')
            sys.exit(1)
        else:
            print('All references are present in the environment.')
