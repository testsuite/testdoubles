#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose2.tools import such

from tests.common.compat import mock
from mockingbird import fake, TestDoubleConfigurationError, get_qualified_name
from tests.common.layers import UnitTestsLayer
from tests.unit.fakes.support import RealObject


with such.A('Fake Object') as it:
    it.uses(UnitTestsLayer)

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

    it.createTests(globals())
