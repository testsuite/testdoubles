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


def is_method_missing(method_name, spec, obj):
    method = getattr(spec, method_name)
    return method_name not in dir(obj) and not method_name.startswith('__') and (
        inspect.ismethod(method) or inspect.isfunction(method) or type(method).__name__ == 'function')


def get_missing_methods(spec, obj):
    return list(filter(lambda method: is_method_missing(method, spec, obj), dir(spec)))


def is_property_missing(prop, spec, obj):
    return prop not in dir(obj) and not prop.startswith('__') and inspect.isdatadescriptor(getattr(spec, prop))


def get_missing_properties(spec, obj):
    return list(filter(lambda prop: is_property_missing(prop, spec, obj), dir(spec)))


def substitute(obj, qualified_name, spec):
    testdouble = mock.patch(qualified_name, spec=spec, spec_set=True, new=obj)
    testdouble.attribute_name = qualified_name

    class FakesPatcher(object):
        new = 1
        
        def _new(*args, **kwargs): 
            return obj.__new__(obj)

        def __enter__(self):
            self._old_new = spec.__new__
            spec.__new__ = self._new
            return obj

        def __exit__(self, exc_type, exc_val, exc_tb):
            spec.__new__ = self._old_new

    testdouble.additional_patchers.append(FakesPatcher())

    return testdouble


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

        attrs.update({method: make_default_implementation(method)})

    properties = get_missing_properties(spec, obj)
    for prop in properties:
        def make_default_implementation(attr):
            def default_implementation(*args, **kwargs):
                raise NotImplementedError('%s was not implemented when the object was faked.' % attr)

            return property(fget=lambda *args, **kwargs: default_implementation(*args, **kwargs),
                            fset=lambda *args, **kwargs: default_implementation(*args, **kwargs),
                            fdel=lambda *args, **kwargs: default_implementation(*args, **kwargs))

        attrs.update({prop: make_default_implementation(prop)})

    fake_qualified_name = get_qualified_name(obj)
    obj = type(obj.__name__, obj.__bases__, attrs)

    return substitute(obj, qualified_name, spec)
