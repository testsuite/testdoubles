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
    try:
        if obj.__module__ not in obj.__qualname__:
            return '%s.%s' % (obj.__module__, obj.__qualname__)

        return obj.__qualname__
    except AttributeError:
        return '%s.%s' % (obj.__module__, obj.__name__)


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
        def make_default_implementation(attr):
            def default_implementation(*args, **kwargs):
                raise NotImplementedError('%s was not implemented when the object was faked.' % attr)

            return default_implementation

        attrs.update({method: make_default_implementation})

    fake_qualified_name = get_qualified_name(obj)
    obj = type(fake_qualified_name, obj.__bases__, attrs)

    return mock.patch(qualified_name, spec=spec, spec_set=True, new=obj)
