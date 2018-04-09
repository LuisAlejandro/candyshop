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
``candyshop.bundle`` is a module for representing Odoo Modules.

This module contains abstraction classes to represent a ``Module`` or a
``Bundle`` (a group of modules). These classes are *read-only*. For now,
you cannot create or modify Bundles or Modules through these abstractions.
"""

from __future__ import print_function

import os
import sys
from ast import literal_eval

from lxml import etree

from .utils import find_files, ModuleProperties, strip_comments_and_blanks

MANIFEST_FILES = ['__odoo__.py', '__openerp__.py', '__terp__.py']
DEFAULT_OCA_USER = 'OCA'
DEFAULT_OCA_BRANCH = '8.0'

if not sys.version_info < (3,):
    basestring = str


class Module(object):
    """
    This class represents an Odoo Module.

    An Odoo module is a method to extend the Odoo codebase, adding or
    customizing functionalities. It is declared through its manifest file,
    and often contains other data files.

    For more information, please refer to official documentation.

    `Modules <https://www.odoo.com/documentation/8.0/howtos/backend.html>`_.
    """

    def __init__(self, path, bundle=None):
        """
        Initialize the ``Module`` instance.

        :param path: a path pointing to the root directory of an Odoo Module.
        :param bundle: a ``Bundle`` instance (indicating this module is part of
                       such bundle), or ``None`` (indicating that is a
                       standalone module).
        :return: a ``Module`` instance.

        .. versionadded:: 0.1.0
        """
        assert os.path.isdir(path), \
            '{0} is not a directory or does not exist.'.format(path)
        assert (isinstance(bundle, Bundle) or not bundle), \
            'Wrong bundle type.'

        #: Attribute ``Module.bundle`` (``Bundle`` or ``None``): Holds the
        #: information regarding the bundle to which this Module belongs.
        self.bundle = bundle

        #: Attribute ``Module.path`` (string): Refers to the absolute path
        #: of the root directory that contains the module.
        self.path = os.path.abspath(path)

        #: Attribute ``Module.manifest`` (string): Refers to the absolute path
        #: to the manifest file of the module (``__openerp__.py``,
        #: ``__odoo__.py`` or ``__terp__.py``).
        self.manifest = self.__get_manifest()

        #: Object ``Module.properties`` (``ModuleProperties``): Placeholder
        #: for the module's properties. Access the module's properties as
        #: attributes of this object.
        self.properties = ModuleProperties(self.__extract_properties())
        self.properties.slug = os.path.basename(self.path)

    def __is_python_package(self):
        """
        Private method to determine if a module is a python package.

        .. versionadded:: 0.1.0
        """
        if find_files(self.path, '__init__.py'):
            return True
        return False

    def __get_manifest(self):
        """
        Private method to find the manifest file within the module.

        .. versionadded:: 0.1.0
        """
        assert self.__is_python_package(), \
            'The module is not a python package.'
        for mfst in MANIFEST_FILES:
            found = find_files(self.path, mfst)
            if not found:
                continue
            return found[0]
        return False

    def __extract_properties(self):
        """
        Private method to extract information of the module's manifest file.

        .. versionadded:: 0.1.0
        """
        assert self.manifest, \
            'The specified path does not contain a manifest file.'
        try:
            with open(self.manifest) as properties:
                props = literal_eval(properties.read())
        except BaseException:
            raise IOError(('An error ocurred while '
                           'reading {0}.').format(self.manifest))
        else:
            return props

    def __xmlfile_isfrom_module(self, xmlfile):
        """
        Private method to determine if a module contains an XML file.

        .. versionadded:: 0.1.0
        """
        return (hasattr(self.properties, 'data') and
                xmlfile.replace('{0}/'.format(self.path), '')
                in self.properties.data)

    def parse_xml_fromfile(self, xmlfile):
        """
        Get XML parsed from an input file.

        :param xmlfile: (string) a path pointing to an XML file.
        :return: Parsed document (``lxml.etree`` object). If there is
                 a syntax error return string error message.

        .. versionadded:: 0.1.0
        """
        assert self.__xmlfile_isfrom_module(xmlfile), \
            'The file {0} does not belong to this module.'.format(xmlfile)
        try:
            doc = etree.parse(xmlfile)
        except etree.XMLSyntaxError as e:
            return e.message
        else:
            return doc

    def get_records_fromfile(self, xmlfile, model=None):
        """
        Get ``record`` tags of an Odoo XML file.

        :param xmlfile: (string) a path pointing to an XML file.
        :param model: (string or None) a record model to filter.
                      If model is None (default) then get all records.
        :return: a list of lxml ``record`` nodes. If there
                 is a syntax error return [].

        .. versionadded:: 0.1.0
        """
        model_filter = ''
        if model:
            model_filter = '[@model="{model}"]'.format(model=model)
        doc = self.parse_xml_fromfile(xmlfile)
        if isinstance(doc, basestring):
            return []
        return (doc.xpath('/openerp//record' + model_filter) +
                doc.xpath('/odoo//record' + model_filter))

    def get_record_ids_fromfile(self, xmlfile, module=None):
        """
        Get ids from `record` tags of an Odoo XML file.

        :param xmlfile: (string) a path pointing to the XML file.
        :param module: (string or None) a record module to filter.
                       If module is None (default) then get all modules.
        :return: a generator that produces an iterable of strings
                 with all ``[MODULE].[ID]`` found.

        .. versionadded:: 0.1.0
        """
        for record in self.get_records_fromfile(xmlfile):
            rid = record.get('id', '').split('.')
            if not rid[0]:
                continue
            if len(rid) == 1:
                xml_module, xml_id = [self.properties.slug, rid[0]]
            else:
                xml_module, xml_id = rid
            if module and xml_module != module:
                continue
            noupdate = record.getparent().get('noupdate', '0')
            yield '{0}.{1}.noupdate={2}'.format(xml_module, xml_id, noupdate)

    def get_record_ids(self):
        """
        Get all record ids contained in all of the module's XML files.

        :return: a generator that returns an iterable of dictionaries
                 containing a list of record ids referenced in each
                 XML file, like this one::

                     [
                        {'path/file1.xml': ['module_a.id_a.noupdate=0']},
                        {'path/file2.xml': ['module_b.id_b.noupdate=0']}
                     ]

        .. versionadded:: 0.1.0
        """
        if not hasattr(self.properties, 'data'):
            return
            yield
        for data in self.properties.data:
            datafile = os.path.join(self.path, data)
            if os.path.splitext(datafile)[1].lower() != '.xml':
                continue
            yield {data: self.get_record_ids_fromfile(datafile)}

    def get_record_ids_module_references(self):
        """
        Get all modules referenced in Odoo XML files.

        :return: a generator that returns an iterable of dictionaries
                 containing a list of modules referenced in each
                 XML file, like this one::

                     [
                        {'path/file1.xml': ['module_a', 'module_b']},
                        {'path/file2.xml': ['module_c']}
                     ]

        .. versionadded:: 0.1.0
        """
        for xmldict in self.get_record_ids():
            for data, ids in xmldict.items():
                record_ids = [i.split('.')[0] for i in ids]
                if not record_ids:
                    continue
                yield {data: list(set(record_ids))}


class Bundle(object):
    """
    This class represents a group of modules or ``Bundle``.

    Also referred as ``Addons``, a group of modules is simply a folder where
    you can put modules. Optionally, it can have a ``oca_dependencies.txt``
    file (located at the root folder), where you can specify other git
    repositories needed for the correct operation of some of the modules
    included in the ``Bundle``.
    """

    def __init__(self, path=None, exclude_tests=True):
        """
        Initialize a ``Bundle`` instance.

        :param path: (string) a path pointing to the root directory containing
                     Odoo Modules.
        :param exclude_tests: (boolean) ``True`` (default) to exclude modules
                              that are inside a ``tests`` folder. ``False`` to
                              include such modules.
        :return: a ``Bundle`` instance.

        .. versionadded:: 0.1.0
        """
        assert os.path.isdir(path), \
            '{0} is not a directory or does not exist.'.format(path)

        #: Attribute ``Bundle.path`` (string): Refers to the absolute path
        #: of the root directory that contains the bundle.
        self.path = os.path.abspath(path)

        #: Attribute ``Bundle.exclude_tests`` (boolean): True if modules
        #: inside a ``tests`` folder will be excluded. False otherwise.
        self.exclude_tests = exclude_tests

        try:
            #: Attribute ``Bundle.modules`` (list): A list containing
            #: instances of ``Module`` for each module inside the bundle.
            self.modules = list(self.__get_modules())
        except BaseException:
            print('The specified path contains broken Odoo Modules.')
            raise
        else:
            assert self.modules, \
                'The specified path does not contain valid Odoo modules.'

            #: Attribute ``Bundle.name`` (string): The name of the bundle.
            self.name = os.path.basename(self.path)

            #: Attribute ``Bundle.oca_dependencies`` (dict): A dictionary
            #: containing key-values of the names and repositories of
            #: OCA dependencies.
            self.oca_dependencies = list(self.__parse_oca_dependencies())

    def __get_modules(self):
        """
        Private method to find and instance all valid modules inside a bundle.

        .. versionadded:: 0.1.0
        """
        for mfst in MANIFEST_FILES:
            for mods in find_files(self.path, mfst):
                if ((self.exclude_tests and
                     'tests' not in mods.split(os.sep)) or
                   not self.exclude_tests):
                    yield Module(os.path.dirname(mods), bundle=self)

    def __get_oca_dependencies_file(self):
        """
        Private method to find (if any) the oca_dependencies.txt file.

        .. versionadded:: 0.1.0
        """
        oca_dependencies_file = os.path.join(self.path, 'oca_dependencies.txt')
        if os.path.isfile(oca_dependencies_file):
            self.oca_dependencies_file = oca_dependencies_file
            return True
        return False

    def __parse_oca_dependencies(self):
        """
        Private method to parse (if any) the oca_dependencies.txt file.

        .. versionadded:: 0.1.0
        """
        if not self.__get_oca_dependencies_file():
            return
            yield
        with open(self.oca_dependencies_file) as f:
            oca = strip_comments_and_blanks(f.read())
        for dep in [o.split() for o in oca.split('\n')]:
            if len(dep) < 2:
                dep.append('https://github.com/{0}/{1}'.format(
                    DEFAULT_OCA_USER, dep[0]))
            if len(dep) < 3:
                dep.append(DEFAULT_OCA_BRANCH)
            yield dep
