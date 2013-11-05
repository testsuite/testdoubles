#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import ArgSpec

from nose2.tools import such

from testdoubles.fakes import callables
from tests.common.compat import mock
from tests.common.layers import UnitTestsLayer
from tests.unit.fakes.support.fakes import fake_live_bound_callable, fake_live_unbound_callable
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

    with it.having('a python 3.x runtime2'):
        @it.has_test_setup
        def setup(case):
            stub_callable(case, True)
            stub_python_version(case, 3)

        @it.has_test_teardown
        def teardown(case):
            unstub_python_version(case)
            unstub_callable(case)

        @it.should("have the same name as the live object")
        def test_should_have_the_same_name_as_the_live_object(case):
            with mock.patch('inspect.ismethod', return_value=True):
                with mock.patch('inspect.isfunction', return_value=True):
                    sut = callables.FakeCallable(object)
                    expected = object.__name__

                    actual = sut.__name__

                    case.assertEqual(actual, expected)

        @it.should("have the same name as the live object when the live object is a callable class instance")
        def test_should_have_the_same_name_as_the_live_object_when_the_live_object_is_a_callable_class_instance(case):
            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.isfunction', return_value=False):
                    with mock.patch('inspect.getargspec', return_value=[]):
                        sut = callables.FakeCallable(mock.DEFAULT)
                        expected = mock.DEFAULT.__class__.__name__

                        actual = sut.__name__

                        case.assertEqual(actual, expected)

        @it.should("have a reference to the instance if the method is bound")
        def test_should_have_a_reference_to_the_instance_if_the_method_is_bound(case):
            live_callable, _ = fake_live_bound_callable()
            expected = live_callable.__self__

            sut = callables.FakeCallable(live_callable)

            actual = sut.__self__

            case.assertEqual(actual, expected)

        @it.should("raise an attribute error when accessing __self__ and the method is not bound")
        def test_should_raise_an_attribute_error_when_accessing_self_and_the_method_is_not_bound(case):
            with case.assertRaisesRegexp(AttributeError,
                                         r"'function' object has no attribute '__self__'"):
                sut = callables.FakeCallable(mock.DEFAULT)

                _ = sut.__self__

        @it.should("raise an attribute error when attempting to use the im_self alias")
        def test_should_raise_an_attribute_error_when_attempting_to_use_the_im_self_alias(case):
            with case.assertRaisesRegexp(AttributeError,
                                         r"'FakeCallable' object has no attribute 'im_self'"):
                sut = callables.FakeCallable(mock.DEFAULT)

                _ = sut.im_self

        @it.should("raise an attribute error when attempting to use the im_class internal attribute")
        def test_should_raise_an_attribute_error_when_attempting_to_use_the_im_class_internal_attribute(case):
            with case.assertRaisesRegexp(AttributeError,
                                         r"'FakeCallable' object has no attribute 'im_class'"):
                sut = callables.FakeCallable(mock.DEFAULT)

                _ = sut.im_class

        @it.should("have a reference to the fake unbound version of the method if the method is bound")
        def test_should_have_a_reference_to_the_fake_unbound_version_of_the_method_if_the_method_is_bound(case):
            live_callable, _ = fake_live_bound_callable()

            sut = callables.FakeCallable(live_callable)
            expected = sut.fake.__func__
            with mock.patch('inspect.ismethod', return_value=True):
                actual = sut.__func__

            case.assertEqual(actual, expected)

        @it.should("not have a reference to the fake unbound version of the method if the method is unbound")
        def test_should_not_have_a_reference_to_the_fake_unbound_version_of_the_method_if_the_method_is_unbound(case):
            live_callable, _ = fake_live_unbound_callable()
            sut = callables.FakeCallable(live_callable)
            expected = None
            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec', return_value=ArgSpec(['self'], None, None, None)):
                    actual = sut.__func__

            case.assertEqual(actual, expected)

        @it.should("raise an attribute error when accessing __func__ and the method is not bound")
        def test_should_raise_an_attribute_error_when_accessing_func_and_the_method_is_not_bound(case):
            with case.assertRaisesRegexp(AttributeError,
                                         r"'function' object has no attribute '__func__'"):
                sut = callables.FakeCallable(mock.DEFAULT)

                _ = sut.__func__

    with it.having('a python 2.x runtime2'):
        @it.has_test_setup
        def setup(case):
            stub_callable(case, True)
            stub_python_version(case, 2)

        @it.has_test_teardown
        def teardown(case):
            unstub_python_version(case)
            unstub_callable(case)

        @it.should("have the same name as the live object")
        def test_should_have_the_same_name_as_the_live_object(case):
            with mock.patch('inspect.ismethod', return_value=True):
                with mock.patch('inspect.isfunction', return_value=True):
                    sut = callables.FakeCallable(object)
                    expected = object.__name__

                    actual = sut.__name__

                    case.assertEqual(actual, expected)

        @it.should("have the same name as the live object when the live object is a callable class instance")
        def test_should_have_the_same_name_as_the_live_object_when_the_live_object_is_a_callable_class_instance(case):
            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.isfunction', return_value=False):
                    sut = callables.FakeCallable(mock.DEFAULT)
                    expected = mock.DEFAULT.__class__.__name__

                    actual = sut.__name__

                    case.assertEqual(actual, expected)

        @it.should("have a reference to the instance if the method is bound")
        def test_should_have_a_reference_to_the_instance_if_the_method_is_bound(case):
            live_callable, _ = fake_live_bound_callable()
            expected = live_callable.__self__

            sut = callables.FakeCallable(live_callable)

            actual = sut.__self__

            case.assertEqual(actual, expected)

        @it.should("raise an attribute error when accessing __self__ and the method is not bound")
        def test_should_raise_an_attribute_error_when_accessing_self_and_the_method_is_not_bound(case):
            with case.assertRaisesRegexp(AttributeError,
                                         r"'function' object has no attribute '__self__'"):
                sut = callables.FakeCallable(mock.DEFAULT)

                _ = sut.__self__

        @it.should("have an attribute named im_self that is equal to the __self__ attribute")
        def test_should_have_an_attribute_named_im_self_that_is_equal_to_the_self_attribute(case):
            live_callable, _ = fake_live_bound_callable()
            expected = live_callable.__self__

            sut = callables.FakeCallable(live_callable)

            actual = sut.im_self

            case.assertEqual(actual, expected)

        @it.should("have an attribute named im_class that is equal to the __self__ attribute's type")
        def test_should_have_an_attribute_named_im_self_that_is_equal_to_the_self_attribute_type(case):
            live_callable, _ = fake_live_bound_callable()
            expected = live_callable.__self__.__class__

            sut = callables.FakeCallable(live_callable)

            actual = sut.im_class

            case.assertEqual(actual, expected)

        @it.should("have a reference to the fake unbound version of the method if the method is bound")
        def test_should_have_a_reference_to_the_fake_unbound_version_of_the_method_if_the_method_is_bound(case):
            live_callable, _ = fake_live_bound_callable()

            sut = callables.FakeCallable(live_callable)
            expected = sut.fake.__func__
            with mock.patch('inspect.ismethod', return_value=True):
                actual = sut.__func__

            case.assertEqual(actual, expected)

        @it.should("not have a reference to the fake unbound version of the method if the method is unbound")
        def test_should_not_have_a_reference_to_the_fake_unbound_version_of_the_method_if_the_method_is_unbound(case):
            live_callable, _ = fake_live_unbound_callable()
            sut = callables.FakeCallable(live_callable)
            expected = None

            with mock.patch('inspect.ismethod', return_value=True):
                actual = sut.__func__

            case.assertEqual(actual, expected)

        @it.should("raise an attribute error when accessing __func__ and the method is not bound")
        def test_should_raise_an_attribute_error_when_accessing_func_and_the_method_is_not_bound(case):
            with case.assertRaisesRegexp(AttributeError,
                                         r"'function' object has no attribute '__func__'"):
                sut = callables.FakeCallable(mock.DEFAULT)

                with mock.patch('inspect.ismethod', return_value=False):
                    _ = sut.__func__

    it.createTests(globals())

with such.A("Fake Function's initialization method") as it:
    it.uses(UnitTestsLayer)

    @it.has_test_setup
    def setup(case):
        stub_callable(case, True)

    @it.has_test_teardown
    def teardown(case):
        unstub_callable(case)

    @it.should("raise a value error when inspecting arguments of a builtin callable")
    def test_should_raise_a_value_error_when_inspecting_arguments_of_a_builtin_callable(case):
        with case.assertRaisesRegexp(ValueError,
                                     r"Cannot inspect arguments of a builtin live object."):
            with mock.patch('inspect.isbuiltin', return_value=True):
                callables.FakeCallable(mock.DEFAULT, inspect_args=True)

    @it.should("raise a value error when the provided live object does not match the argspec")
    def test_should_raise_a_value_error_when_the_provided_live_object_does_not_match_the_argspec(case):
        stub_are_argspecs_identical(case, False)

        with case.assertRaisesRegexp(ValueError,
                                     r"The provided live object's arguments ArgSpec\((?:[a-zA-Z1-9_]+=.+(?:, |(?=\))))+\) does not match ArgSpec\((?:[a-zA-Z1-9_]+=.+(?:, |(?=\))))+\)"):
            with mock.patch('inspect.getargspec', return_value=ArgSpec(['a'], None, None, (None,))):
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
            mocked_callable, self = fake_live_bound_callable()

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
            mocked_callable, self = fake_live_bound_callable()

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
            mocked_callable, self = fake_live_bound_callable()

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=True):
                actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return false if the live function is a bound instance method")
        def test_should_return_false_if_the_live_function_is_a_bound_instance_method(case):
            mocked_callable, self = fake_live_bound_callable()

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
            mocked_callable, self = fake_live_bound_callable()

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=True):
                _ = sut.is_unbound_instance_method
                self.assert_called_once_with()

    it.createTests(globals())