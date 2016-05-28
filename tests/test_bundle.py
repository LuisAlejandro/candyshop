#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_candyshop
----------------------------------

Tests for `candyshop` module.
"""


import os
import unittest

from candyshop.bundle import ModulesBundle, Module


class TestModulesBundle(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(__file__)
        self.bundledir = os.path.join(self.testdir, 'examples', 'bundle')
        self.odoo_afr_dir = os.path.join(self.bundledir, 'odoo-afr')
        # self.moduledir = os.path.join(self.testdir, 'examples', 'module')

    def tearDown(self):
        pass

    def test_01_get_modules(self):
        def modules_name_list(instance):
            for module in instance.modules:
                yield module.name

        odoo_afr = ModulesBundle(self.odoo_afr_dir)
        odoo_afr_modules_should_be = ['account_afr_group_auditory',
                                      'account_financial_report']
        self.assertListEqual(list(modules_name_list(odoo_afr)),
                             odoo_afr_modules_should_be)

    def test_02_modules_are_instances_of_module(self):
        odoo_afr = ModulesBundle(self.odoo_afr_dir)
        for module in odoo_afr.modules:
            self.assertIsInstance(module, Module)

    def test_03_get_oca_dependencies(self):
        odoo_afr = ModulesBundle(self.odoo_afr_dir)
        oca_dependencies_file_should_be = os.path.join(self.odoo_afr_dir,
                                                       'oca_dependencies.txt')
        self.assertEqual(odoo_afr.oca_dependencies_file,
                         oca_dependencies_file_should_be)

    def test_04_parse_oca_dependencies(self):
        odoo_afr = ModulesBundle(self.odoo_afr_dir)
        oca_dependencies_should_be = {'addons-vauxoo':'https://github.com/Vauxoo/addons-vauxoo.git'}
        self.assertDictEqual(odoo_afr.oca_dependencies,
                             oca_dependencies_should_be)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
