#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose2.tools import such
from testdoubles.fakes.function import FakeFunction
from tests.common.compat import mock
from tests.common.layers import UnitTestsLayer

with such.A("Fake Function's live property") as it:
    it.uses(UnitTestsLayer)

    @it.should("have a read only property named live")
    def test_should_have_a_read_only_property_named_live(case):
        sut = FakeFunction(mock.DEFAULT)

        with case.assertRaises(AttributeError):
            sut.live = mock.sentinel.VALUE

    @it.should("be equal to the provided function")
    def test_should_have_a_read_only_property_named_live(case):
        sut = FakeFunction(mock.DEFAULT)

        case.assertEqual(sut.live, mock.DEFAULT)

    it.createTests(globals())

with such.A("Fake Function's is instance method property") as it:
    it.uses(UnitTestsLayer)

    @it.should("return true if the live function is an instance method")
    def test_should_return_true_if_the_live_function_is_an_instance_method(case):
        sut = FakeFunction(mock.DEFAULT)

        with mock.patch('inspect.ismethod', return_value=True):
            with mock.patch('inspect.getargspec', return_value=([], )):
                actual = sut.is_instance_method

        case.assertTrue(actual)

    @it.should("return true if the live function is an unbound instance method")
    def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
        sut = FakeFunction(mock.DEFAULT)

        with mock.patch('inspect.ismethod', return_value=False):
            with mock.patch('inspect.getargspec', return_value=(('self', ), )):
                actual = sut.is_instance_method

        case.assertTrue(actual)

    @it.should("return false if the live function is not an instance method")
    def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
        sut = FakeFunction(mock.DEFAULT)

        with mock.patch('inspect.ismethod', return_value=False):
            with mock.patch('inspect.getargspec', return_value=([], )):
                actual = sut.is_instance_method

        case.assertEqual(actual, False)

    it.createTests(globals())