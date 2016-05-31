
import os
import fnmatch


def get_path(path=[]):
    """

    Build and normalize a path. This will resolve symlinks to their
    destination and convert relative to absolute paths.

    This function does not check if the python path really exists.

    :param path: a list with the components of a path.
    :return: the full path.
    :rtype: a string.

    .. versionadded:: 0.1.0

    >>> p = ['/usr', 'share', 'logs/vars', 'included', 'hola.deb']
    >>> get_path(p)
    '/usr/share/logs/vars/included/hola.deb'

    """
    assert type(path) == list
    return os.path.normpath(os.path.realpath(
        os.path.abspath(os.path.join(*path))))


def find_files(path=None, pattern='*'):
    """

    Locate all the files matching the supplied filename pattern in and below
    the supplied root directory. If no pattern is supplied, all files will be
    returned.

    :param path: a string containing a path where the files will be looked for.
    :param pattern: a string containing a regular expression.
    :return: a list of files matching the pattern within path (recursive).
    :rtype: a list.

    .. versionadded:: 0.1.0

    """
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
