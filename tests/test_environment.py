# -*- coding: utf-8 -*-
#
# Please refer to AUTHORS.rst for a complete list of Copyright holders.
# Copyright (C) 2016-2022, Candyshop Developers.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import doctest
import unittest
from io import StringIO
from contextlib import contextmanager

from candyshop.environment import Environment


@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out


class TestEnvironment(unittest.TestCase):

    def setUp(self):

        self.testdir = os.path.dirname(os.path.abspath(__file__))
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.odoo_afr_dir = os.path.join(self.exampledir, 'odoo-afr')
        self.odoo_beginners_dir = os.path.join(self.exampledir,
                                               'odoo-beginners')
        self.odoo = Environment(branch=os.environ.get('ODOO_BRANCH', '15.0'))

    def tearDown(self):
        self.odoo.destroy()

    def bundle_name_list(self, environment):
        for bundle in environment.bundles:
            yield bundle.name

    def test_01_initialization(self):
        self.assertListEqual(sorted(list(self.bundle_name_list(self.odoo))),
                             sorted(['addons', 'addons']))

    def test_02_addbundles(self):
        self.odoo.addbundles([self.odoo_afr_dir, self.odoo_beginners_dir],
                             False)
        self.assertListEqual(sorted(list(self.bundle_name_list(self.odoo))),
                             sorted(['addons', 'addons', 'addons-vauxoo',
                                     'odoo-afr', 'odoo-beginners']))

    def test_03_unexistent_record_ids(self):
        notmet_record_ids_should_be = [{
            'odoo-beginners': {
                'references_absent_ids/view/test.xml': ['unexistent_module']
            }
        }]
        notmet_record_ids_report_should_be = (
            'The following record ids are not found in the environment:\n\n'
            '    Bundle: odoo-beginners\n'
            '    XML file: references_absent_ids/view/test.xml\n'
            '    Missing references:\n'
            '        - unexistent_module\n\n'
        )

        sys.exit = lambda *args: None
        self.odoo.reset()
        self.odoo.addbundles([self.odoo_beginners_dir], False)
        self.assertListEqual(list(self.odoo.get_notmet_record_ids()),
                             notmet_record_ids_should_be)
        with capture(self.odoo.get_notmet_record_ids_report) as output:
            self.assertMultiLineEqual(notmet_record_ids_report_should_be,
                                      output)

    def test_04_unexistent_dependency(self):
        notmet_dependencies_should_be = [{
            'odoo-beginners': {
                'missing_dependency': ['unexistent_dependency']
            }
        }]
        notmet_dependencies_report_should_be = (
            'The following module dependencies are not '
            'found in the environment:\n\n'
            '    Bundle: odoo-beginners\n'
            '    Module: missing_dependency\n'
            '    Missing dependencies:\n'
            '        - unexistent_dependency\n\n'
        )

        sys.exit = lambda *args: None
        self.odoo.reset()
        self.odoo.addbundles([self.odoo_beginners_dir], False)
        self.assertListEqual(list(self.odoo.get_notmet_dependencies()),
                             notmet_dependencies_should_be)
        with capture(self.odoo.get_notmet_dependencies_report) as output:
            self.assertMultiLineEqual(notmet_dependencies_report_should_be,
                                      output)

    def test_05_satisfy_oca_dependencies(self):
        self.odoo.reset()
        self.odoo.addbundles([self.odoo_afr_dir], False)
        self.assertIn('addons-vauxoo', list(self.bundle_name_list(self.odoo)))


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite('candyshop.environment'))
    return tests


if __name__ == '__main__':
    sys.exit(unittest.main())
