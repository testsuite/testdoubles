#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources
from mockingbird.compat import mock

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

    qualified_name = spec.__qualname__ if hasattr(spec, '__qualname__') else '%s.%s' % (spec.__class__.__module__, spec.__class__.__name__)

    return mock.patch(qualified_name, spec_set=spec, new=obj)
