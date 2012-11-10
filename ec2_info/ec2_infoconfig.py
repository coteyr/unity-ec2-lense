# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# THIS IS Ec2Info CONFIGURATION FILE
# YOU CAN PUT THERE SOME GLOBAL VALUE
# Do not touch unless you know what you're doing.
# you're warned :)

__all__ = [
    'project_path_not_found',
    'get_data_file',
    'get_data_path',
    ]

# Where your project will look for your data (for instance, images and ui
# files). By default, this is ../data, relative your trunk layout
__ec2_info_data_directory__ = '/usr/share/ec2-info/'
__license__ = ''
__version__ = '0.2'

import os

import locale
from locale import gettext as _
locale.textdomain('ec2-info')

class project_path_not_found(Exception):
    """Raised when we can't find the project directory."""


def get_data_file(*path_segments):
    """Get the full path to a data file.

    Returns the path to a file underneath the data directory (as defined by
    `get_data_path`). Equivalent to os.path.join(get_data_path(),
    *path_segments).
    """
    return os.path.join(get_data_path(), *path_segments)


def get_data_path():
    """Retrieve ec2-info data path

    This path is by default <ec2_info_lib_path>/../data/ in trunk
    and /usr/share/ec2-info in an installed version but this path
    is specified at installation time.
    """

    # Get pathname absolute or relative.
    path = os.path.join(
        os.path.dirname(__file__), __ec2_info_data_directory__)

    abs_data_path = os.path.abspath(path)
    if not os.path.exists(abs_data_path):
        raise project_path_not_found

    return abs_data_path
