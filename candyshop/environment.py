
from sh import git

from .modules import ModulesBundle


class Environment(object):

    def __init__(self, bundles=[]):
        self.bundles = bundles

    def insert_bundles(self, locations=[]):
        for location in locations:
            try:
                self.bundles.append(ModulesBundle(location))
            except BaseException as e:
                raise e(('There was a problem inserting the bundle'
                         ' located at %s') % location)

    def satisfy_oca_dependencies(self):
        for bundle in self.bundles:
            for name, repo in bundle.oca_dependencies:
                self.git_clone(repo, os.path.join(bundle.path, name))
            bundle.refresh()

    def git_clone(self, repo, path):
        git.clone(repo, depth=1, path)


