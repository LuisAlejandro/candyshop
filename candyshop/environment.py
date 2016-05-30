
import os
import tempfile

from sh import git

from .modules import ModulesBundle

DEFAULT_REPO = 'https://github.com/vauxoo/odoo'
DEFAULT_BRANCH = '8.0'


class OdooEnvironment(object):

    def __init__(self, repo=DEFAULT_REPO, branch=DEFAULT_BRANCH):
        self.bundles = []
        self.initialize_odoo(repo, branch)

    def initialize_odoo(self, repo, branch):
        odoo_dir = tempfile.mkdtemp()
        self.git_clone(repo, branch, odoo_dir)
        self.insert_bundles([
            os.path.join(odoo_dir, 'addons'),
            os.path.join(odoo_dir, 'openerp', 'addons')
        ])

    def insert_bundles(self, locations=[]):
        for location in locations:
            try:
                self.bundles.append(ModulesBundle(location))
            except BaseException as e:
                raise type(e)(('There was a problem inserting the bundle'
                               ' located at %s') % location)

    def satisfy_oca_dependencies(self):
        for bundle in self.bundles:
            for name, repo in bundle.oca_dependencies:
                new_bundle_dir = tempfile.mkdtemp()
                self.git_clone(repo, new_bundle_dir)
                self.insert_bundles([new_bundle_dir])

    def git_clone(self, repo, branch, path):
        git.clone(repo, path, quiet=True, single_branch=True,
                  depth=1, branch=branch)

    def get_modules_list(self):
        for bundle in self.bundles:
            for module in bundle.modules:
                yield module

    def get_modules_slug_list(self):
        for bundle in self.bundles:
            for module in bundle.modules:
                yield module.properties.slug

    def get_notmet_dependencies(self):
        for module in self.get_modules_list():
            notmetlist = []
            for dep in module.properties.depends:
                if dep not in set(self.get_modules_slug_list()):
                    notmetlist.append(dep)
            yield {module.properties.slug: notmetlist}

    def get_notmet_record_ids(self):
        for module in self.get_modules_list():
            notmetlist = []
            for ref in set(module.get_record_ids_module_references()):
                if ref not in set(self.get_modules_slug_list()):
                    notmetlist.append(ref)
            yield {module.properties.slug: notmetlist}
