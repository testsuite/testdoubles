#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imp import reload
from unittest import expectedFailure
from nose2.tools import such
from testdoubles.fakes import callable
from tests.common.compat import mock
from tests.common.layers import UnitTestsLayer

with such.A("Fake Function's live property") as it:
    it.uses(UnitTestsLayer)

    @it.should("have a read only property named live")
    def test_should_have_a_read_only_property_named_live(case):
        sut = callable.FakeCallable(mock.DEFAULT)

        with case.assertRaises(AttributeError):
            sut.live = mock.sentinel.VALUE

    @it.should("be equal to the provided function")
    def test_should_have_a_read_only_property_named_live(case):
        sut = callable.FakeCallable(mock.DEFAULT)

        case.assertEqual(sut.live, mock.DEFAULT)

    it.createTests(globals())

with such.A("Fake Function's is instance method property") as it:
    it.uses(UnitTestsLayer)

    with it.having('a python 3.x runtime'):
        @it.has_test_setup
        def setup(case):
            case.patch_python_version = mock.patch('testdoubles.fakes.callable.python3', new_callable=mock.PropertyMock, return_value=True)
            case.patch_python_version.start()

            reload(callable)

        @it.has_test_teardown
        def teardown(case):
            case.patch_python_version.stop()

            reload(callable)

        @it.should("return true if the live function is an instance method")
        def test_should_return_true_if_the_live_function_is_an_instance_method(case):
            sut = callable.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=True):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return true if the live function is an unbound instance method")
        def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
            sut = callable.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=(('self', ), )):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return false if the live function is not an instance method")
        def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
            sut = callable.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertEqual(actual, False)

        @it.should("detect unbound instance methods by inspecting the arguments")
        def test_should_detect_unbound_instance_methods_by_inspecting_the_arguments(case):
            sut = callable.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec') as mocked_getargspec:
                    _ = sut.is_unbound_instance_method
                    mocked_getargspec.assert_called_once_with(sut.live)

        @it.should("not detect unbound instance methods by inspecting their self attribute")
        def test_should_not_detect_unbound_instance_methods_by_inspecting_their_self_attribute(case):
            mocked_callable = mock.MagicMock()
            type(mocked_callable).__self__ = mock.PropertyMock()

            sut = callable.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec'):
                    _ = sut.is_unbound_instance_method
                    mocked_callable.__self__.assert_has_calls([])

    with it.having('a python 2.x runtime'):
        @it.has_test_setup
        def setup(case):
            case.patch_python_version = mock.patch('testdoubles.fakes.callable.python3', new_callable=mock.PropertyMock, return_value=False)
            case.patch_python_version.start()

            reload(callable)

        @it.has_test_teardown
        def teardown(case):
            case.patch_python_version.stop()

            reload(callable)

        @it.should("return true if the live function is an instance method")
        def test_should_return_true_if_the_live_function_is_an_instance_method(case):
            sut = callable.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=True):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return true if the live function is an unbound instance method")
        def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
            sut = callable.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=(('self', ), )):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return false if the live function is not an instance method")
        def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
            sut = callable.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertEqual(actual, False)

        @it.should("not detect unbound instance methods by inspecting the arguments")
        def test_should_not_detect_unbound_instance_methods_by_inspecting_the_arguments(case):
            sut = callable.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec') as mocked_getargspec:
                    _ = sut.is_unbound_instance_method
                    mocked_getargspec.assert_calls(sut.live)

        @it.should("detect unbound instance methods by inspecting their self attribute")
        @expectedFailure
        def test_should_detect_unbound_instance_methods_by_inspecting_their_self_attribute(case):
            mocked_callable = mock.MagicMock()
            type(mocked_callable).__self__ = mock.PropertyMock()

            sut = callable.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=False):
                    _ = sut.is_unbound_instance_method
                    mocked_callable.__self__.assert_called_once_with()

    it.createTests(globals())