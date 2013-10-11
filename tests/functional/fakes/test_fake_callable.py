#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose2.tools import such
from testdoubles.fakes.callables import FakeCallable
from tests.common.layers import FunctionalTestsLayer
from tests.common.compat import mock

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
    def test_should_not_raise_a_ValueError_when_the_provided_live_object_does_not_match_the_argspec(case):
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