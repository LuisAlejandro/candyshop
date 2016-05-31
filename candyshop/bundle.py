from __future__ import print_function

import os
from ast import literal_eval

from lxml import etree

from .utils import find_files

MANIFEST_FILES = ['__odoo__.py', '__openerp__.py', '__terp__.py']

try:
    basestring
except NameError:
    basestring = str


class ModuleProperties(object):
    def __init__(self, data):
        for key in data:
            setattr(self, key, data[key])


class Module(object):

    def __init__(self, bundle=None, path=None):
        assert os.path.isdir(path), \
            '%s is not a directory or does not exist.' % path
        assert (isinstance(bundle, ModulesBundle) or not bundle), \
            'Wrong bundle type.'

        self.bundle = bundle
        self.path = os.path.abspath(path)
        self.manifest = self.get_manifest()
        self.is_package = self.is_python_package()

        assert self.manifest, \
            'The specified path does not contain a manifest file.'
        assert self.is_package, 'The module is not a python package.'

        self.properties = ModuleProperties(self.extract_properties())
        self.properties.slug = os.path.basename(self.path)

    def extract_properties(self):
        try:
            with open(self.manifest) as properties:
                props = literal_eval(properties.read())
        except BaseException:
            raise IOError('An error ocurred while reading %s.' % self.manifest)
        else:
            return props

    def is_python_package(self):
        if find_files(self.path, '__init__.py'):
            return True
        return False

    def get_manifest(self):
        """return False if the path doesn't contain an odoo module, and the full
        path to the module manifest otherwise"""
        for mfst in MANIFEST_FILES:
            found = find_files(self.path, mfst)
            if found:
                return found[0]
        return False

    def get_record_ids_module_references(self):
        for xmldict in self.get_record_ids():
            for data, ids in xmldict.items():
                record_ids = list(set([id.split('.')[0] for id in ids]))
                if record_ids:
                    yield {data: record_ids}

    def get_record_ids(self):
        if hasattr(self.properties, 'data'):
            for data in self.properties.data:
                datafile = os.path.join(self.path, data)
                if os.path.splitext(datafile)[1].lower() == '.xml':
                    yield {data: self.get_record_ids_fromfile(datafile)}

    def xmlfile_isfrom_module(self, xmlfile):
        return hasattr(self.properties, 'data') and \
            xmlfile.replace('%s/' % self.path, '') in self.properties.data

    def parse_xml_fromfile(self, xmlfile):
        """
        Get xml parsed from an input file.

        :param xmlfile: Path of the XML file.
        :return: Parsed document (`lxml.etree` object). If there is
                 a syntax error return string error message
        """
        assert self.xmlfile_isfrom_module(xmlfile), \
            'The file %s does not belong to this module.' % xmlfile
        try:
            with open(xmlfile) as x:
                doc = etree.parse(x)
        except etree.XMLSyntaxError as e:
            return e.message
        else:
            return doc

    def get_records_fromfile(self, xmlfile, model=None):
        """
        Get `record` tags of an Odoo XML file.

        :param xmlfile: Path of the XML file.
        :param model: String with record model to filter.
                      If model is None then get all.
                      Default None.
        :return: List of lxml `record` nodes. If there
                 is a syntax error return [].
        """
        model_filter = ''
        if model:
            model_filter = "[@model='{model}']".format(model=model)
        doc = self.parse_xml_fromfile(xmlfile)
        if isinstance(doc, basestring):
            return []
        return (doc.xpath("/openerp//record" + model_filter) +
                doc.xpath("/odoo//record" + model_filter))

    def get_record_ids_fromfile(self, xmlfile, module=None):
        """
        Get ids from `record` tags of an Odoo XML file.

        :param xmlfile: Path of the XML file.
        :param module: String with record module to filter.
                       If module is None then get all.
                       Default None.
        :return: List of strings with `[MODULE].[ID]` found.
        """
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


class ModulesBundle(object):

    def __init__(self, path=None, exclude_tests=True):
        assert os.path.isdir(path), \
            '%s is not a directory or does not exist.' % path

        self.path = os.path.abspath(path)
        self.exclude_tests = exclude_tests

        try:
            self.modules = list(self.get_modules())
        except BaseException:
            print('The specified path contains broken Odoo Modules.')
            raise
        else:
            assert self.modules, \
                'The specified path does not contain valid Odoo modules.'
            self.name = os.path.basename(self.path)
            self.oca_dependencies = self.parse_oca_dependencies()

    def get_modules(self):
        for mfst in MANIFEST_FILES:
            for mods in find_files(self.path, mfst):
                if self.exclude_tests:
                    if 'tests' not in mods.split(os.sep):
                        yield Module(self, os.path.dirname(mods))
                else:
                    yield Module(self, os.path.dirname(mods))

    def get_oca_dependencies_file(self):
        oca_dependencies_file = os.path.join(self.path, 'oca_dependencies.txt')
        if os.path.isfile(oca_dependencies_file):
            self.oca_dependencies_file = oca_dependencies_file
            return True
        return False

    def parse_oca_dependencies(self):
        if self.get_oca_dependencies_file():
            with open(self.oca_dependencies_file) as oca:
                deps = [d.split() for d in oca.read().split('\n')]
            return {k: v for k, v in filter(None, deps)}
        return {}
