# -*- coding: utf-8 -*-
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
candyshop.utils module
----------------------

'''

import os
import fnmatch


class ModuleProperties(object):
    '''
    .. versionadded:: 0.1.0

    This class holds the properties of a module. It recieves a Dictionary and
    converts it to class attributes for better access.

    :param data: a dictionary containing the properties of a module as specified
                 in the manifest file of an Odoo Module.
    :return: each key-value is assigned as an attribute to this class.

    For example:

    >>> p = ModuleProperties({'name': 'Vauxoo Module'})
    >>> p.name
    Vauxoo Module
    '''
    def __init__(self, data):
        for key in data:
            setattr(self, key, data[key])


def get_path(path=[]):
    '''
    .. versionadded:: 0.1.0

    Build and normalize a path. This will resolve symlinks to their
    destination and convert relative to absolute paths.

    This function does not check if the python path really exists.

    :param path: a list with the components of a path.
    :return: a string indicating the full path.

    For example:

    >>> p = ['/usr', 'share', 'logs/vars', 'included', 'hola.txt']
    >>> get_path(p)
    /usr/share/logs/vars/included/hola.txt
    '''
    assert type(path) == list
    return os.path.normpath(os.path.realpath(
        os.path.abspath(os.path.join(*path))))


def find_files(path=None, pattern='*'):
    '''
    .. versionadded:: 0.1.0

    Locate all the files matching the supplied filename pattern in and below
    the supplied root directory. If no pattern is supplied, all files will be
    returned.

    :param path: a string containing a path where the files will be looked for.
    :param pattern: a string containing a regular expression.
    :return: a list of files matching the pattern within path (recursive).
    '''
    d = []
    assert type(path) == str
    assert type(pattern) == str
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for filename in fnmatch.filter(files, pattern):
            if os.path.isfile(os.path.join(directory, filename)):
                if os.path.islink(os.path.join(directory, filename)):
                    d.append(os.path.join(get_path([directory]), filename))
                else:
                    d.append(get_path([directory, filename]))
    return d
