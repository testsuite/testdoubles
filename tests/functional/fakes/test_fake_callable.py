#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose2.tools import such
from testdoubles.fakes.callable import FakeCallable
from tests.common.layers import FunctionalTestsLayer

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