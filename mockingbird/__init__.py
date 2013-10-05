#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
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


def get_qualified_name(obj):
    return obj.__qualname__ if hasattr(obj, '__qualname__') else '%s.%s' % (
        obj.__class__.__module__, obj.__class__.__name__)


def is_method_missing(method, spec, obj):
    return method not in dir(obj) and not method.startswith('__') and inspect.ismethod(getattr(spec, method))


def get_missing_methods(spec, obj):
    return list(filter(lambda method: is_method_missing(method, spec, obj), dir(spec)))


def fake(obj):
    """


    :rtype : mock._patch
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

    qualified_name = get_qualified_name(spec)

    attrs = dict(obj.__dict__)
    attrs.pop('Configuration')

    methods = get_missing_methods(spec, obj)
    for method in methods:
        def default_implementation(*args, attr=method, **kwargs):
            raise NotImplementedError('%s was not implemented when the object was faked.' % attr)

        attrs.update({method: default_implementation})

    fake_qualified_name = get_qualified_name(obj)
    obj = type(fake_qualified_name, obj.__bases__, attrs)

    return mock.patch(qualified_name, spec_set=spec, new=obj)
