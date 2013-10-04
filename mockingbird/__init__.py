#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources

__author__ = 'Omer Katz'
__email__ = 'omer.drow@gmail.com'

try:
    __version__ = pkg_resources.get_distribution('mockingbird').version
except pkg_resources.DistributionNotFound:
    __version__ = ''


def fake(obj):
    """

    :param obj:
    """

    if not hasattr(obj, 'Configuration'):
        raise TypeError('A fake testdouble must have a Configuration class.')
