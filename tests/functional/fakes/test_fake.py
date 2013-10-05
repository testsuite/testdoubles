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

        spec = FakeObject.Configuration().spec

        with fake(FakeObject) as fake_type:
            fake_obj = fake_type()

            case.assertTrue(fake_obj.was_faked())

    it.createTests(globals())
