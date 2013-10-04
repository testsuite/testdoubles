#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mockingbird.compat import mock
import pkg_resources

__author__ = 'Omer Katz'
__email__ = 'omer.drow@gmail.com'

try:
    __version__ = pkg_resources.get_distribution('mockingbird').version
except pkg_resources.DistributionNotFound:
    __version__ = ''


class TestDoubleConfigurationError(RuntimeError):
    pass


def fake(obj):
    """

    :param obj:
    """
    try:
        configuration = obj.Configuration()
    except AttributeError:
        raise TypeError('A fake testdouble must have a Configuration class.')

    try:
        spec = configuration.spec
    except AttributeError:
            raise TestDoubleConfigurationError('The type to be faked was not specified.')

    testdouble = mock.Mock(spec_set=spec)
