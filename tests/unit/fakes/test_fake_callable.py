#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose2.tools import such

from testdoubles.fakes import callables
from tests.common.compat import mock
from tests.common.layers import UnitTestsLayer
from tests.unit.fakes.support.fakes import fake_real_callable
from tests.unit.fakes.support.mocks import mock_are_argspecs_identical, unmock_are_argspecs_identical
from tests.unit.fakes.support.stubs import stub_callable, unstub_callable, stub_are_argspecs_identical, unstub_are_argspecs_identical, stub_python_version, unstub_python_version

with such.A("Fake Function object") as it:
    it.uses(UnitTestsLayer)

    @it.has_test_setup
    def setup(case):
        stub_callable(case, True)

    @it.has_test_teardown
    def teardown(case):
        unstub_callable(case)

    @it.should("be callable")
    def test_should_be_callable(case):
        sut = callables.FakeCallable(mock.DEFAULT)

        callable = case.old_callable
        case.assertTrue(callable(sut))

    it.createTests(globals())

with such.A("Fake Function's initialization method") as it:
    it.uses(UnitTestsLayer)

    @it.has_test_setup
    def setup(case):
        stub_callable(case, True)

    @it.has_test_teardown
    def teardown(case):
        unstub_callable(case)

    @it.should("raise a value error when the provided live object does not match the argspec")
    def test_should_raise_a_value_error_when_the_provided_live_object_does_not_match_the_argspec(case):
        stub_are_argspecs_identical(case, False)

        with case.assertRaisesRegexp(ValueError,
                                     r"The provided live object's arguments ArgSpec\((?:[a-zA-Z1-9_]+=.+(?:, |(?=\))))+\) does not match ArgSpec\((?:[a-zA-Z1-9_]+=.+(?:, |(?=\))))+\)"):
            with mock.patch('inspect.getargspec', return_value='ArgSpec(a=None)'):
                callables.FakeCallable(mock.DEFAULT, inspect_args=True)

        unstub_are_argspecs_identical(case)

    @it.should("not raise a value error when the provided live object matches the argspec")
    def test_should_not_raise_a_value_error_when_the_provided_live_object_matches_the_argspec(case):
        stub_are_argspecs_identical(case, True)

        try:
            callables.FakeCallable(mock.DEFAULT, inspect_args=True)
        except ValueError:
            case.fail()

        unstub_are_argspecs_identical(case)

    @it.should("not inspect the argspec of the live object when argument inspection is opted out")
    def test_should_not_inspect_the_argspec_of_the_live_object_when_argument_inspection_is_opted_out(case):
        mocked_are_argspecs_identical = mock.Mock()

        mock_are_argspecs_identical(case, mocked_are_argspecs_identical)

        try:
            callables.FakeCallable(mock.DEFAULT, inspect_args=False)
        except ValueError:
            pass

        mocked_are_argspecs_identical.assert_has_calls([])

        unmock_are_argspecs_identical(case)

    it.createTests(globals())

with such.A("Fake Function's live property") as it:
    it.uses(UnitTestsLayer)

    @it.has_test_setup
    def setup(case):
        stub_callable(case, True)

    @it.has_test_teardown
    def teardown(case):
        unstub_callable(case)

    @it.should("have a read only property named live")
    def test_should_have_a_read_only_property_named_live(case):
        sut = callables.FakeCallable(mock.DEFAULT)

        with case.assertRaises(AttributeError):
            sut.live = mock.sentinel.VALUE

    @it.should("be equal to the provided function")
    def test_should_have_a_read_only_property_named_live(case):
        sut = callables.FakeCallable(mock.DEFAULT)

        case.assertEqual(sut.live, mock.DEFAULT)

    it.createTests(globals())

with such.A("Fake Function's fake property") as it:
    it.uses(UnitTestsLayer)

    @it.has_test_setup
    def setup(case):
        stub_callable(case, True)

    @it.has_test_teardown
    def teardown(case):
        unstub_callable(case)

    @it.should("have a read only property named fake")
    def test_should_have_a_read_only_property_named_live(case):
        sut = callables.FakeCallable(mock.DEFAULT)

        with case.assertRaises(AttributeError):
            sut.fake = mock.sentinel.VALUE

    @it.should("be equal to the bound __call__ of the fake callable")
    def test_should_have_a_read_only_property_named_live(case):
        sut = callables.FakeCallable(mock.DEFAULT)

        case.assertEqual(sut.fake, sut.fake)

    it.createTests(globals())

with such.A("Fake Function's is instance method property") as it:
    it.uses(UnitTestsLayer)

    with it.having('a python 3.x runtime1'):
        @it.has_test_setup
        def setup(case):
            stub_python_version(case, 3)

            stub_callable(case, True)

        @it.has_test_teardown
        def teardown(case):
            unstub_python_version(case)

            unstub_callable(case)

        @it.should("return true if the live function is an instance method")
        def test_should_return_true_if_the_live_function_is_an_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)
            with mock.patch('inspect.ismethod', return_value=True):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return true if the live function is an unbound instance method")
        def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=(('self', ), )):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return false if the live function is not an instance method")
        def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertEqual(actual, False)

    with it.having('a python 2.x runtime1'):
        @it.has_test_setup
        def setup(case):
            stub_python_version(case, 2)

            stub_callable(case, True)

        @it.has_test_teardown
        def teardown(case):
            unstub_python_version(case)

            unstub_callable(case)

        @it.should("return true if the live function is an instance method")
        def test_should_return_true_if_the_live_function_is_an_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=True):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return true if the live function is an unbound instance method")
        def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
            mocked_callable, self = fake_real_callable()

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=True):
                actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return false if the live function is not an instance method")
        def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertEqual(actual, False)

    it.createTests(globals())

with such.A("Fake Function's is unbound instance method property") as it:
    it.uses(UnitTestsLayer)

    with it.having('a python 3.x runtime'):
        @it.has_test_setup
        def setup(case):
            stub_python_version(case, 3)

            stub_callable(case, True)

        @it.has_test_teardown
        def teardown(case):
            unstub_python_version(case)

            unstub_callable(case)

        @it.should("return true if the live function is an unbound instance method")
        def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=(('self', ), )):
                    actual = sut.is_unbound_instance_method

            case.assertTrue(actual)

        @it.should("return false if the live function is a bound an instance method")
        def test_should_return_false_if_the_live_function_is_a_bound_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=True):
                with mock.patch('inspect.getargspec', return_value=(['self'], )):
                    actual = sut.is_unbound_instance_method

            case.assertEqual(actual, False)

        @it.should("return false if the live function is not an instance method")
        def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=([''], )):
                    actual = sut.is_unbound_instance_method

            case.assertEqual(actual, False)

        @it.should("detect unbound instance methods by inspecting the arguments")
        def test_should_detect_unbound_instance_methods_by_inspecting_the_arguments(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec') as mocked_getargspec:
                    _ = sut.is_unbound_instance_method
                    mocked_getargspec.assert_called_once_with(sut.live)

        @it.should("not detect unbound instance methods by inspecting their self attribute")
        def test_should_not_detect_unbound_instance_methods_by_inspecting_their_self_attribute(case):
            mocked_callable, self = fake_real_callable()

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec'):
                    _ = sut.is_unbound_instance_method
                    self.assert_has_calls([])

    with it.having('a python 2.x runtime'):
        @it.has_test_setup
        def setup(case):
            stub_python_version(case, 2)

            stub_callable(case, True)

        @it.has_test_teardown
        def teardown(case):
            unstub_python_version(case)

            unstub_callable(case)

        @it.should("return true if the live function is an unbound instance method")
        def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
            mocked_callable, self = fake_real_callable()

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=True):
                actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return false if the live function is a bound instance method")
        def test_should_return_false_if_the_live_function_is_a_bound_instance_method(case):
            mocked_callable, self = fake_real_callable()

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=True):
                actual = sut.is_unbound_instance_method

            case.assertEqual(actual, False)


        @it.should("return false if the live function is not an instance method")
        def test_should_return_false_if_the_live_function_is_not_an_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertEqual(actual, False)

        @it.should("not detect unbound instance methods by inspecting the arguments")
        def test_should_not_detect_unbound_instance_methods_by_inspecting_the_arguments(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec') as mocked_getargspec:
                    _ = sut.is_unbound_instance_method
                    mocked_getargspec.assert_calls(sut.live)

        @it.should("detect unbound instance methods by inspecting their self attribute")
        def test_should_detect_unbound_instance_methods_by_inspecting_their_self_attribute(case):
            mocked_callable, self = fake_real_callable()

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=True):
                _ = sut.is_unbound_instance_method
                self.assert_called_once_with()

    it.createTests(globals())