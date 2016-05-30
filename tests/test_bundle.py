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


class TestModule(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(__file__)
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.odoo_afr_dir = os.path.join(self.exampledir, 'odoo-afr')
        self.broken_manifest_dir = os.path.join(self.exampledir, 'broken-manifest')
        self.is_not_package_dir = os.path.join(self.exampledir, 'is-not-package',
                                               'is_not_package')
        self.non_existent_dir = os.path.join(self.exampledir, 'non-existent')
        self.empty_dir = os.path.join(self.exampledir, 'empty')
        self.openacademy_project_dir = os.path.join(self.exampledir, 'odoo-beginners',
                                                    'openacademy-project')

    def test_01_is_python_package(self):
        openacademy_project = Module(None, self.openacademy_project_dir)
        self.assertTrue(openacademy_project.is_python_package())

    def test_02_is_not_python_package(self):
        self.assertRaisesRegexp(
            AssertionError, 'The module is not a python package.',
            Module, None, self.is_not_package_dir
        )

    def test_03_match_properties(self):
        openacademy = Module(None, self.openacademy_project_dir)
        self.assertEqual(openacademy.properties.name, 'Open Academy')
        self.assertEqual(openacademy.properties.version, '0.1')
        self.assertListEqual(openacademy.properties.depends, ['base', 'board'])

    def test_04_get_record_ids_module_references(self):
        openacademy = Module(None, self.openacademy_project_dir)
        self.assertListEqual(openacademy.get_record_ids_module_references(),
                             ['openacademy-project'])

    # def test_02_is_python_package(self):
    # def test_02_is_python_package(self):
    # def test_02_is_python_package(self):


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
        self.assertRaisesRegexp(
            AssertionError, '%s is not a directory or does not exist.' % self.non_existent_dir,
            ModulesBundle, self.non_existent_dir
        )

    def test_02_empty_bundle(self):
        self.assertRaisesRegexp(
            AssertionError, 'The specified path does not contain valid Odoo modules.',
            ModulesBundle, self.empty_dir
        )

    def test_03_broken_manifest(self):
        self.assertRaisesRegexp(
            IOError, 'An error ocurred while reading.*',
            ModulesBundle, self.broken_manifest_dir
        )

    def test_04_is_not_package(self):
        self.assertRaisesRegexp(
            AssertionError, 'The module is not a python package.',
            ModulesBundle, self.is_not_package_dir
        )



if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
