#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect

from nose2.tools import such

from tests.common.compat import mock
from mockingbird import fake, TestDoubleConfigurationError, get_qualified_name, get_missing_methods


with such.A('Fake Object') as it:
    @it.should('raise a TypeError when the configuration does not exist')
    def test_should_raise_type_error_when_configuration_does_not_exist(case):
        with case.assertRaisesRegexp(TypeError, 'A fake testdouble must have a Configuration class.'):
            fake(object)

    @it.should('raise a TestDoubleConfigurationError when the configuration does not contain the type to be faked')
    def test_should_raise_test_double_configuration_error_when_configuration_does_contain_spec(case):
        class FakeObject(object):
            class Configuration(object):
                pass

        with case.assertRaisesRegexp(TestDoubleConfigurationError, 'The type to be faked was not specified.'):
            fake(FakeObject)

    @it.should('create a new patch object with the configured spec')
    def test_should_create_a_new_mock_object_with_the_configured_spec(case):
        class FakeObject(object):
            class Configuration(object):
                spec = mock.Mock()

        spec = FakeObject.Configuration().spec

        with mock.patch('tests.common.compat.mock.patch') as m:
            fake(FakeObject)

            qualified_name = get_qualified_name(spec)

            m.assert_called_once_with(qualified_name, spec_set=spec, new=mock.ANY)

    @it.should('contain all methods that are missing in the fake implementation')
    def test_should_contain_all_methods(case):
        class FakeObject(object):
            class Configuration(object):
                spec = mock.Mock()

        spec = FakeObject.Configuration().spec

        with fake(FakeObject):
            fake_obj = mock.Mock()

            case.assertEqual(
                list(
                    filter(lambda a: not a.startswith('__') and inspect.ismethod(getattr(fake_obj, a)), dir(fake_obj))),
                list(filter(lambda a: not a.startswith('__') and inspect.ismethod(getattr(spec, a)), dir(spec))))

    @it.should('raise NotImplementedError when invoking any method that is missing in the fake implementation')
    def test_should_raise_not_implemented_error_when_invoking_missing_methods(case):
        class FakeObject(object):
            class Configuration(object):
                spec = mock.Mock()

        spec = FakeObject.Configuration().spec

        with fake(FakeObject):
            fake_obj = mock.Mock()

            missing_methods = get_missing_methods(spec, FakeObject)

            for method_name in missing_methods:
                method = getattr(fake_obj, method_name)

                with case.assertRaisesRegexp(NotImplementedError,
                                             '%s was not implemented when the object was faked.' % method_name):
                    method()


    it.createTests(globals())
