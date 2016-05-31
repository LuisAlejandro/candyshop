# -*- coding: utf-8 -*-
'''
candyshop.environment
---------------------

'''


import os
import tempfile

from sh import git

from .bundle import ModulesBundle

DEFAULT_REPO = 'https://github.com/vauxoo/odoo'
DEFAULT_BRANCH = '8.0'


class OdooEnvironment(object):

    def __init__(self, init=True, init_from=None,
                 repo=DEFAULT_REPO, branch=DEFAULT_BRANCH):

        self.bundles = []
        self.tempdir = tempfile.mkdtemp()

        if init:
            self.initialize_odoo(repo, branch, init_from)

    def initialize_odoo(self, repo, branch, init_from):
        if init_from:
            odoo_dir = os.path.abspath(init_from)
        else:
            odoo_dir = os.path.join(self.tempdir, 'odoo')
            self.git_clone(repo, branch, odoo_dir)
        self.insert_bundles([
            os.path.join(odoo_dir, 'addons'),
            os.path.join(odoo_dir, 'openerp', 'addons')
        ])

    def insert_bundles(self, locations=[], exclude_tests=True):
        for location in locations:
            location = os.path.abspath(location)
            if location not in self.get_bundle_path_list():
                try:
                    self.bundles.append(ModulesBundle(location, exclude_tests))
                except BaseException:
                    print(('There was a problem inserting the bundle'
                           ' located at %s') % location)
                    raise

    def clear_bundles(self):
        self.bundles = []

    def satisfy_oca_dependencies(self):
        for bundle in self.bundles:
            for name, repo in bundle.oca_dependencies.items():
                bundle_dir = os.path.join(self.tempdir, name)
                if not os.path.isdir(bundle_dir):
                    self.git_clone(repo=repo, branch=DEFAULT_BRANCH,
                                   path=bundle_dir)
                    self.insert_bundles([bundle_dir])
                    self.satisfy_oca_dependencies()

    def git_clone(self, repo, branch, path):
        try:
            git.clone(repo, path, quiet=True, depth=1, branch=branch)
        except BaseException:
            print('There was a problem cloning %s.' % repo)
            raise

    def get_bundle_path_list(self):
        for bundle in self.bundles:
            yield bundle.path

    def get_modules_slug_list(self):
        for bundle in self.bundles:
            for module in bundle.modules:
                yield module.properties.slug

    def generate_notmet_dependencies(self):
        for i, bundle in enumerate(self.bundles):
            for j, module in enumerate(bundle.modules):
                notmetlist = []
                if hasattr(module.properties, 'depends'):
                    for dep in module.properties.depends:
                        if dep not in set(self.get_modules_slug_list()):
                            notmetlist.append(dep)
                    if notmetlist:
                        self.bundles[i].modules[j].notmet_dependencies = notmetlist

    def get_notmet_dependencies(self):
        self.generate_notmet_dependencies()
        for bundle in self.bundles:
            moduledict = {}
            for module in bundle.modules:
                if hasattr(module, 'notmet_dependencies'):
                    moduledict[module.properties.slug] = module.notmet_dependencies
            if moduledict:
                yield {bundle.name: moduledict}

    def generate_notmet_record_ids(self):
        for i, bundle in enumerate(self.bundles):
            for j, module in enumerate(bundle.modules):
                notmetlist = []
                for ref in set(module.get_record_ids_module_references()):
                    if ref not in set(self.get_modules_slug_list()):
                        notmetlist.append(ref)
                if notmetlist:
                    self.bundles[i].modules[j].notmet_record_ids = notmetlist

    def get_notmet_record_ids(self):
        self.generate_notmet_record_ids()
        for bundle in self.bundles:
            moduledict = {}
            for module in bundle.modules:
                if hasattr(module, 'notmet_record_ids'):
                    moduledict[module.properties.slug] = module.notmet_record_ids
            if moduledict:
                yield {bundle.name: moduledict}

