

from lxml import etree

MANIFEST_FILES = ['__odoo__.py', '__openerp__.py', '__terp__.py']

class AddOn(object):
    def __init__(self, path):
        self.path = path
        if self.is_addon():
            self.manifest = self.get_addon_manifest()
            self.properties = self.extract_addons_properties()
        else:
            raise OSError('The specified path does not contain an Odoo Module.')

    def extract_addons_properties(self):
        assert self.manifest, 'This is not an addon or it hasn\'t been properly initialized.'
        try:
            with open(self.manifest) as properties:
                self.properties = eval(properties.read())
        except BaseException as e:
            raise e('An error ocurred while reading %s' % self.manifest)

    def is_addon(self):
        assert self.path, 'This is not an addon or it hasn\'t been properly initialized.'
        return self.get_addon_manifest()

    def get_addon_manifest(self):
        """return False if the path doesn't contain an odoo module, and the full
        path to the module manifest otherwise"""
        assert self.path, 'This is not an addon or it hasn\'t been properly initialized.'

        if not os.path.isdir(path):
            return False
        files = os.listdir(path)
        filtered = [x for x in files if x in (MANIFEST_FILES + ['__init__.py'])]
        if len(filtered) == 2 and '__init__.py' in filtered:
            return os.path.join(
                path, next(x for x in filtered if x != '__init__.py'))
        else:
            return False

    def parse_xml(self, xml_file):
        """Get xml parsed.
        :param xml_file: Path of file xml
        :return: Doc parsed (lxml.etree object)
            if there is syntax error return string error message
        """
        try:
            doc = etree.parse(open(xml_file))
        except etree.XMLSyntaxError as xmlsyntax_error_exception:
            return xmlsyntax_error_exception.message
        return doc

    def get_xml_records(self, xml_file, model=None):
        """Get tag `record` of a openerp xml file.
        :param xml_file: Path of file xml
        :param model: String with record model to filter.
                      if model is None then get all.
                      Default None.
        :return: List of lxml `record` nodes
            If there is syntax error return []
        """
        if model is None:
            model_filter = ''
        else:
            model_filter = "[@model='{model}']".format(model=model)
        doc = self.parse_xml(xml_file)
        return doc.xpath("/openerp//record" + model_filter) + \
            doc.xpath("/odoo//record" + model_filter) \
            if not isinstance(doc, basestring) else []

    def get_xml_record_ids(self, xml_file, module=None):
        """Get xml ids from tags `record of a openerp xml file
        :param xml_file: Path of file xml
        :param model: String with record model to filter.
                      if model is None then get all.
                      Default None.
        :return: List of string with module.xml_id found
        """
        xml_ids = []
        for record in self.get_xml_records(xml_file):
            xml_module, xml_id = record.get('id').split('.') \
                if '.' in record.get('id') \
                else [self.module, record.get('id')]
            if module and xml_module != module:
                continue
            # Support case where using two xml_id:
            #  1) With noupdate="1"
            #  2) With noupdate="0"
            noupdate = "noupdate=" + record.getparent().get('noupdate', '0')
            xml_ids.append(
                xml_module + '.' + xml_id + '.' + noupdate)
        return xml_ids
