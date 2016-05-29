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
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.odoo_afr_dir = os.path.join(self.exampledir, 'odoo-afr')

    def test_01_get_modules(self):
        def modules_slug_list(instance):
            for module in instance.modules:
                yield module.properties.slug

        odoo_afr = ModulesBundle(self.odoo_afr_dir)
        odoo_afr_modules_should_be = ['account_afr_group_auditory',
                                      'account_financial_report']
        self.assertListEqual(list(modules_slug_list(odoo_afr)),
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

    def test_05_modules_reference_bundle_instances(self):
        odoo_afr = ModulesBundle(self.odoo_afr_dir)
        for module in odoo_afr.modules:
            self.assertIsInstance(module.bundle, ModulesBundle)
            self.assertEqual(module.bundle.name, 'odoo-afr')


class TestBrokenModulesBundle(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(__file__)
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.broken_manifest_dir = os.path.join(self.exampledir, 'broken-manifest')
        self.is_not_package_dir = os.path.join(self.exampledir, 'is-not-package')
        self.non_existent_dir = os.path.join(self.exampledir, 'non-existent')
        self.empty_dir = os.path.join(self.exampledir, 'empty')

    def test_01_non_existent_bundle(self):
        self.assertRaisesRegex(
            AssertionError, '%s is not a directory or does not exist.' % self.non_existent_dir,
            ModulesBundle, self.non_existent_dir
        )

    def test_02_empty_bundle(self):
        self.assertRaisesRegex(
            AssertionError, 'The specified path does not contain valid Odoo modules.',
            ModulesBundle, self.empty_dir
        )

    def test_03_broken_manifest(self):
        self.assertRaisesRegex(
            IOError, 'An error ocurred while reading.*',
            ModulesBundle, self.broken_manifest_dir
        )

    def test_04_is_not_package(self):
        self.assertRaisesRegex(
            AssertionError, 'The module is not a python package.',
            ModulesBundle, self.is_not_package_dir
        )



if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
