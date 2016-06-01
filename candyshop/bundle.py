#   -*- coding: utf-8 -*-
#   This file is part of Odoo Candyshop
#   ------------------------------------------------------------------------
#   Copyright:
#   Copyright (C) 2016 Vauxoo (<http://vauxoo.com>)
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
candyshop.bundle module
-----------------------

This module contains abstraction classes to represent a ``Module`` or a
``Bundle`` (a group of modules). These classes are *read-only*. For now,
you cannot create or modify Bundles or Modules through these abstractions.

'''

from __future__ import print_function

import os
from ast import literal_eval

from lxml import etree

from .utils import find_files, ModuleProperties

MANIFEST_FILES = ['__odoo__.py', '__openerp__.py', '__terp__.py']

try:
    basestring
except NameError:
    basestring = str


class Module(object):
    '''
    .. versionadded:: 0.1.0

    This class represents an Odoo Module.

    :param path: a path pointing to the root directory of an Odoo Module.
    :param bundle: a ``Bundle`` instance (indicating this module is part of such
                   bundle), or ``None`` (indicating that is a standalone
                   module).
    :return: a ``Module`` instance.
    '''
    def __init__(self, path, bundle=None):
        assert os.path.isdir(path), \
            '%s is not a directory or does not exist.' % path
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
        '''
        .. versionadded:: 0.1.0

        Private method to determine if a module is a python package.
        '''
        if find_files(self.path, '__init__.py'):
            return True
        return False

    def __get_manifest(self):
        '''
        .. versionadded:: 0.1.0

        Private method to find the manifest file within the module.
        '''
        assert self.__is_python_package(), 'The module is not a python package.'
        for mfst in MANIFEST_FILES:
            found = find_files(self.path, mfst)
            if found:
                return found[0]
        return False

    def __extract_properties(self):
        '''
        .. versionadded:: 0.1.0

        Private method to extract information of the module's manifest file.
        '''
        assert self.manifest, \
            'The specified path does not contain a manifest file.'
        try:
            with open(self.manifest) as properties:
                props = literal_eval(properties.read())
        except BaseException:
            raise IOError('An error ocurred while reading %s.' % self.manifest)
        else:
            return props

    def __xmlfile_isfrom_module(self, xmlfile):
        '''
        .. versionadded:: 0.1.0

        Private method to determine if a module contains an XML file.
        '''
        return hasattr(self.properties, 'data') and \
            xmlfile.replace('%s/' % self.path, '') in self.properties.data

    def parse_xml_fromfile(self, xmlfile):
        '''
        .. versionadded:: 0.1.0

        Get XML parsed from an input file.

        :param xmlfile: (string) a path pointing to an XML file.
        :return: Parsed document (``lxml.etree`` object). If there is
                 a syntax error return string error message.
        '''
        assert self.__xmlfile_isfrom_module(xmlfile), \
            'The file %s does not belong to this module.' % xmlfile
        try:
            with open(xmlfile) as x:
                doc = etree.parse(x)
        except etree.XMLSyntaxError as e:
            return e.message
        else:
            return doc

    def get_records_fromfile(self, xmlfile, model=None):
        '''
        .. versionadded:: 0.1.0

        Get ``record`` tags of an Odoo XML file.

        :param xmlfile: (string) a path pointing to an XML file.
        :param model: (string or None) a record model to filter.
                      If model is None (default) then get all records.
        :return: a list of lxml ``record`` nodes. If there
                 is a syntax error return [].
        '''
        model_filter = ''
        if model:
            model_filter = '[@model="{model}"]'.format(model=model)
        doc = self.parse_xml_fromfile(xmlfile)
        if isinstance(doc, basestring):
            return []
        return (doc.xpath('/openerp//record' + model_filter) +
                doc.xpath('/odoo//record' + model_filter))

    def get_record_ids_fromfile(self, xmlfile, module=None):
        '''
        .. versionadded:: 0.1.0

        Get ids from `record` tags of an Odoo XML file.

        :param xmlfile: (string) a path pointing to the XML file.
        :param module: (string or None) a record module to filter.
                       If module is None (default) then get all modules.
        :return: a generator that produces an iterable of strings
                 with all ``[MODULE].[ID]`` found.
        '''
        for record in self.get_records_fromfile(xmlfile):
            id = record.get('id', '').split('.')
            if id[0]:
                if len(id) == 1:
                    xml_module, xml_id = [self.properties.slug, id[0]]
                else:
                    xml_module, xml_id = id
                if module and xml_module != module:
                    continue
                noupdate = record.getparent().get('noupdate', '0')
                yield '%s.%s.noupdate=%s' % (xml_module, xml_id, noupdate)

    def get_record_ids(self):
        '''
        .. versionadded:: 0.1.0

        Get all record ids contained in all of the module's XML files.

        :return: a generator that returns an iterable of dictionaries
                 containing a list of record ids referenced in each
                 XML file, like this one::

                     [
                        {'file1.xml': ['module_a.id_a.noupdate=0']},
                        {'file2.xml': ['module_b.id_b.noupdate=0']}
                     ]
        '''
        if hasattr(self.properties, 'data'):
            for data in self.properties.data:
                datafile = os.path.join(self.path, data)
                if os.path.splitext(datafile)[1].lower() == '.xml':
                    yield {data: self.get_record_ids_fromfile(datafile)}

    def get_record_ids_module_references(self):
        '''
        .. versionadded:: 0.1.0

        Get all modules referenced in Odoo XML files.

        :return: a generator that returns an iterable of dictionaries
                 containing a list of modules referenced in each
                 XML file, like this one::

                     [
                        {'file1.xml': ['module_a', 'module_b']},
                        {'file2.xml': ['module_c']}
                     ]
        '''
        for xmldict in self.get_record_ids():
            for data, ids in xmldict.items():
                record_ids = list(set([id.split('.')[0] for id in ids]))
                if record_ids:
                    yield {data: record_ids}


class Bundle(object):
    '''
    .. versionadded:: 0.1.0

    This class represents a group of modules.

    :param path: (string) a path pointing to the root directory containing
                 Odoo Modules.
    :param exclude_tests: (boolean) ``True`` (default) to exclude modules
                          that are inside a ``tests`` folder. ``False`` to
                          include such modules.
    :return: a ``Bundle`` instance.
    '''
    def __init__(self, path=None, exclude_tests=True):
        assert os.path.isdir(path), \
            '%s is not a directory or does not exist.' % path

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
            self.oca_dependencies = self.__parse_oca_dependencies()

    def __get_modules(self):
        '''
        .. versionadded:: 0.1.0

        Private method to find and instance all valid modules inside a bundle.
        '''
        for mfst in MANIFEST_FILES:
            for mods in find_files(self.path, mfst):
                if self.exclude_tests:
                    if 'tests' not in mods.split(os.sep):
                        yield Module(os.path.dirname(mods), bundle=self)
                else:
                    yield Module(os.path.dirname(mods), bundle=self)

    def __get_oca_dependencies_file(self):
        '''
        .. versionadded:: 0.1.0

        Private method to find (if any) the oca_dependencies.txt file.
        '''
        oca_dependencies_file = os.path.join(self.path, 'oca_dependencies.txt')
        if os.path.isfile(oca_dependencies_file):
            self.oca_dependencies_file = oca_dependencies_file
            return True
        return False

    def __parse_oca_dependencies(self):
        '''
        .. versionadded:: 0.1.0

        Private method to parse (if any) the oca_dependencies.txt file.
        '''
        if self.__get_oca_dependencies_file():
            with open(self.oca_dependencies_file) as oca:
                deps = [d.split() for d in oca.read().split('\n')]
            return {k: v for k, v in filter(None, deps)}
        return {}
