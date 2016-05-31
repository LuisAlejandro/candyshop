#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_environment
----------------

Tests for the `candyshop.environment` module.
"""

from __future__ import print_function

import os
import doctest
import unittest

from candyshop.environment import OdooEnvironment


class TestOdooEnvironment(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(__file__)
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.odoo_afr_dir = os.path.join(self.exampledir, 'odoo-afr')
        self.odoo_beginners_dir = os.path.join(self.exampledir, 'odoo-beginners')
        self.odoo = OdooEnvironment(init_from='/tmp/tmpRM4abx')

    def bundle_name_list(self, environment):
        for bundle in environment.bundles:
            yield bundle.name

    def test_01_initialization(self):
        self.assertListEqual(list(self.bundle_name_list(self.odoo)),
                             ['addons', 'addons'])

    def test_02_insert_bundles(self):
        self.odoo.insert_bundles([self.odoo_afr_dir, self.odoo_beginners_dir], False)
        self.assertListEqual(list(self.bundle_name_list(self.odoo)),
                             ['addons', 'addons', 'odoo-afr', 'odoo-beginners'])


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite('candyshop.environment'))
    return tests

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
