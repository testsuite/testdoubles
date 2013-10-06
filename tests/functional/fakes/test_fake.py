#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
from nose2.tools import such

from tests.common.compat import mock
from mockingbird import fake, get_missing_methods
from tests.common.layers import FunctionalTestsLayer
from tests.functional.fakes.support import RealObject


with such.A('Fake Object') as it:
    it.uses(FunctionalTestsLayer)

    @it.should('substitute the real object with the fake object')
    def test_should_substitute(case):
        class FakeObject(object):
            class Configuration(object):
                spec = RealObject

        with fake(FakeObject) as f:
            case.assertEqual(f().__class__.__name__, FakeObject.__name__)
            case.assertEqual(RealObject().__class__.__name__, FakeObject.__name__)

    @it.should('contain all methods that are missing in the fake implementation')
    def test_should_contain_all_methods(case):
        class FakeObject(object):
            class Configuration(object):
                spec = RealObject

        spec = FakeObject.Configuration().spec

        with fake(FakeObject):
            fake_obj = RealObject

            case.assertEqual(
                list(
                    filter(lambda a: not a.startswith('__') and inspect.ismethod(getattr(fake_obj, a)), dir(fake_obj))),
                list(filter(lambda a: not a.startswith('__') and inspect.ismethod(getattr(spec, a)), dir(spec))))

    @it.should('raise NotImplementedError when invoking any method that is missing in the fake implementation')
    def test_should_raise_not_implemented_error_when_invoking_missing_methods(case):
        class FakeObject(object):
            class Configuration(object):
                spec = str

        spec = FakeObject.Configuration().spec

        with fake(FakeObject):
            fake_obj = mock.Mock()

            missing_methods = get_missing_methods(spec, FakeObject)

            for method_name in missing_methods:
                method = getattr(fake_obj, method_name)

                with case.assertRaisesRegexp(NotImplementedError,
                                             '%s was not implemented when the object was faked.' % method_name):
                    method()

    @it.should('replace the original methods with the fake methods')
    def test_should_replace_the_original_methods_with_the_fake_methods(case):
        class FakeObject(object):
            class Configuration(object):
                spec = RealObject

            def was_faked(self):
                return True

        with fake(FakeObject):
            fake_obj = RealObject()

            case.assertTrue(fake_obj.was_faked())

    @it.should('replace the original properties with the fake properties')
    def test_should_replace_the_original_properties_with_the_fake_properties(case):
        class FakeObject(object):
            class Configuration(object):
                spec = RealObject

            def __init__(self, *args, **kwargs):
                self._fake = 0

            @property
            def real(self):
                return self._fake

            @real.setter
            def real(self, value):
                self._fake = value

        with fake(FakeObject):
            fake_obj = RealObject()

            fake_obj._fake = 1
            case.assertEqual(fake_obj.real, 1)

            fake_obj.real = 2
            case.assertEqual(fake_obj.real, 2)

    @it.should('contain all properties that are missing in the fake implementation')
    def test_should_contain_all_properties(case):
        class FakeObject(object):
            class Configuration(object):
                spec = RealObject

            def __init__(self, *args, **kwargs):
                pass

        spec = FakeObject.Configuration().spec

        with fake(FakeObject):
            fake_obj = RealObject

            expected = list(filter(lambda a: not a.startswith('__') and inspect.isdatadescriptor(getattr(fake_obj, a)),
                                   dir(fake_obj)))
            outcome = list(
                filter(lambda a: not a.startswith('__') and inspect.isdatadescriptor(getattr(spec, a)), dir(spec)))
            case.assertEqual(expected, outcome)

    @it.should(
        'raise NotImplementedError when getting or setting any property that is missing in the fake implementation')
    def test_should_raise_not_implemented_error_when_getting_or_setting_missing_properties(case):
        class FakeObject(object):
            class Configuration(object):
                spec = RealObject

            def __init__(self, *args, **kwargs):
                pass

        with fake(FakeObject):
            fake_obj = RealObject()

            with case.assertRaisesRegexp(NotImplementedError,
                                         'real was not implemented when the object was faked.'):
                _ = fake_obj.real

            with case.assertRaisesRegexp(NotImplementedError,
                                         'real was not implemented when the object was faked.'):
                fake_obj.real = mock.Mock()

    it.createTests(globals())
