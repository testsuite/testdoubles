#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tests.common.compat import mock
from nose2.tools import such
from mockingbird import fake, TestDoubleConfigurationError

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

    @it.should('create a new mock object with the configured spec')
    def test_should_create_a_new_mock_object_with_the_configured_spec(case):
        class FakeObject(object):
            class Configuration(object):
                spec = mock.Mock()
        spec = FakeObject.Configuration().spec

        with mock.patch('tests.common.compat.mock.Mock') as m:
            fake(FakeObject)

            m.assert_called_once_with(spec_set=spec)

    it.createTests(globals())
