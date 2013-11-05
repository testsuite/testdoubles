#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import ArgSpec
from unittest import skipUnless
from nose2.tools import such
import six
from testdoubles.fakes.callables import FakeCallable
from tests.common.layers import FunctionalTestsLayer
from tests.common.compat import mock

with such.A("Fake Function object") as it:
    it.uses(FunctionalTestsLayer)

    @it.should("have the same name as the live object")
    def test_should_have_the_same_name_as_the_live_object(case):
        def foo(): pass

        sut = FakeCallable(foo)
        expected = foo.__name__

        actual = sut.__name__

        case.assertEqual(actual, expected)
        
    @it.should("have the same name as the live object when the live object is a callable class instance")
    def test_should_have_the_same_name_as_the_live_object_when_the_live_object_is_a_callable_class_instance(case):
        class Foo(object):
            def __call__(self, *args, **kwargs):
                pass

        sut = FakeCallable(Foo())
        expected = Foo.__name__

        actual = sut.__name__

        case.assertEqual(actual, expected)
        
    @it.should("have a reference to the instance if the method is bound")
    def test_should_have_a_reference_to_the_instance_if_the_method_is_bound(case):
        class Foo(object):
            def bar(self):
                pass

        live_bound_method = Foo().bar
        expected = live_bound_method.__self__

        sut = FakeCallable(live_bound_method)

        actual = sut.__self__

        case.assertEqual(actual, expected)

    @it.should("raise an attribute error when accessing __self__ and the method is not a bound or unbound instance method")
    def test_should_raise_an_attribute_error_when_accessing_self_and_the_method_is_not_a_bound_or_unbound_instance_method(case):
        def foo():
            pass

        live_unbound_method = foo

        with case.assertRaisesRegexp(AttributeError,
                                     r"'function' object has no attribute '__self__'"):
            sut = FakeCallable(live_unbound_method)

            _ = sut.__self__

    @it.should("raise an attribute error when attempting to use the im_self alias")
    @skipUnless(six.PY3, 'Test should only be run under Python 3.x')
    def test_should_raise_an_attribute_error_when_attempting_to_use_the_im_self_alias(case):
        class Foo(object):
            def bar(self):
                pass

        live_unbound_method = Foo.bar

        sut = FakeCallable(live_unbound_method)

        with case.assertRaisesRegexp(AttributeError,
                                     r"'FakeCallable' object has no attribute 'im_self'"):

            _ = sut.im_self

    @it.should("raise an attribute error when attempting to use the im_class internal attribute")
    @skipUnless(six.PY3, 'Test should only be run under Python 3.x')
    def test_should_raise_an_attribute_error_when_attempting_to_use_the_im_class_internal_attribute(case):
        class Foo(object):
            def bar(self):
                pass

        live_unbound_method = Foo.bar

        sut = FakeCallable(live_unbound_method)

        with case.assertRaisesRegexp(AttributeError,
                                     r"'FakeCallable' object has no attribute 'im_class'"):

            _ = sut.im_class

    @it.should("have an attribute named im_self that is equal to the __self__ attribute")
    @skipUnless(not six.PY3, 'Test should only be run under Python 2.x')
    def test_should_have_an_attribute_named_im_self_that_is_equal_to_the_self_attribute(case):
        class Foo(object):
            def bar(self):
                pass

        live_bound_method = Foo().bar
        expected = live_bound_method.__self__

        sut = FakeCallable(live_bound_method)

        actual = sut.im_self

        case.assertEqual(actual, expected)

    @it.should("have an attribute named im_class that is equal to the __self__ attribute's type")
    @skipUnless(not six.PY3, 'Test should only be run under Python 2.x')
    def test_should_have_an_attribute_named_im_self_that_is_equal_to_the_self_attribute_type(case):
        class Foo(object):
            def bar(self):
                pass

        live_bound_method = Foo().bar
        expected = live_bound_method.__self__.__class__

        sut = FakeCallable(live_bound_method)

        actual = sut.im_class

        case.assertEqual(actual, expected)

    @it.should("have a reference to the fake unbound version of the method if the method is bound")
    def test_should_have_a_reference_to_the_fake_unbound_version_of_the_method_if_the_method_is_bound(case):
        class Foo(object):
            def bar(self):
                pass

        live_bound_method = Foo().bar

        sut = FakeCallable(live_bound_method)
        expected = sut.fake.__func__
        actual = sut.__func__

        case.assertEqual(actual, expected)

    @it.should("not have a reference to the fake unbound version of the method if the method is unbound")
    def test_should_not_have_a_reference_to_the_fake_unbound_version_of_the_method_if_the_method_is_unbound(case):
        class Foo(object):
            def bar(self):
                pass

        live_unbound_method = Foo.bar

        sut = FakeCallable(live_unbound_method)
        expected = None

        actual = sut.__func__

        case.assertEqual(actual, expected)

    @it.should("raise an attribute error when accessing __func__ and the method is not a bound or unbound instance method")
    def test_should_raise_an_attribute_error_when_accessing_func_and_the_method_is_not_a_bound_or_unbound_instance_method(case):
        def foo():
            pass

        live_unbound_method = foo

        with case.assertRaisesRegexp(AttributeError,
                                     r"'function' object has no attribute '__func__'"):
            sut = FakeCallable(live_unbound_method)

            _ = sut.__func__

    it.createTests(globals())

with such.A("Fake Function's initialization method") as it:
    it.uses(FunctionalTestsLayer)

    @it.should("raise a TypeError when the provided live object is not callable")
    def test_should_raise_a_TypeError_when_the_provided_live_object_is_not_callable(case):
        with case.assertRaisesRegexp(TypeError, r"[a-zA-Z1-9_]* is not callable"):
            FakeCallable(mock.NonCallableMagicMock())

    @it.should("raise a ValueError when the provided live object does not match the argspec")
    def test_should_raise_a_ValueError_when_the_provided_live_object_does_not_match_the_argspec(case):
        with case.assertRaisesRegexp(ValueError, r"The provided live object's arguments ArgSpec\((?:[a-zA-Z1-9_]+=.+(?:, |(?=\))))+\) does not match ArgSpec\((?:[a-zA-Z1-9_]+=.+(?:, |(?=\))))+\)"):
            def foo(): pass

            FakeCallable(foo, inspect_args=True)

    @it.should("not raise a ValueError when arguments inspection is opted out.")
    def test_should_not_raise_a_ValueError_when_argument_inspection_is_opted_out(case):
        def foo(): pass

        try:
            FakeCallable(foo, inspect_args=False)
        except ValueError:
            case.fail()


    it.createTests(globals())

with such.A("Fake Function's object initialization method") as it:
    it.uses(FunctionalTestsLayer)

    @it.should("raise a TypeError when the provided live object is not callable")
    def test_should_raise_a_TypeError_when_the_provided_live_object_is_not_callable(case):
        with case.assertRaisesRegexp(TypeError, r"[a-zA-Z1-9_]* is not callable"):
            FakeCallable(mock.NonCallableMagicMock())

with such.A("Fake Function's is instance method property") as it:
    it.uses(FunctionalTestsLayer)

    @it.should("return true if the live function is an instance method")
    def test_should_return_true_if_the_live_function_is_an_instance_method(case):
        class klass(object):
            def function(self):
                pass

        sut = FakeCallable(klass().function)

        case.assertTrue(sut.is_instance_method)

    @it.should("return true if the live function is an unbound instance method")
    def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
        class klass(object):
            def function(self):
                pass

        sut = FakeCallable(klass.function)

        case.assertTrue(sut.is_instance_method)

    @it.should("return false if the live function is not an instance method")
    def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
        def function():
            pass

        sut = FakeCallable(function)

        case.assertEqual(sut.is_instance_method, False)

    it.createTests(globals())

with such.A("Fake Function's is unbound instance method property") as it:
    it.uses(FunctionalTestsLayer)

    @it.should("return false if the live function is an instance method")
    def test_should_return_false_if_the_live_function_is_an_instance_method(case):
        class klass(object):
            def function(self):
                pass

        sut = FakeCallable(klass().function)

        case.assertEqual(sut.is_unbound_instance_method, False)

    @it.should("return true if the live function is an unbound instance method")
    def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
        class klass(object):
            def function(self):
                pass

        sut = FakeCallable(klass.function)

        case.assertTrue(sut.is_unbound_instance_method)

    @it.should("return false if the live function is not an instance method")
    def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
        def function():
            pass

        sut = FakeCallable(function)

        case.assertEqual(sut.is_unbound_instance_method, False)

    it.createTests(globals())