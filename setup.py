from __future__ import division, print_function, absolute_import

import sys


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('scobra',parent_package,top_path)
    config.add_subpackage('analysis')
    config.add_subpackage('classes')
    config.add_subpackage('cyc')
    config.add_subpackage('io')
    config.add_subpackage('manipulation')
    # config.add_subpackage('build')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())

# Must install other depedencies such as pandas apparently, numpy, scipy, cobra, matplotlib