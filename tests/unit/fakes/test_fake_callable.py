#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imp import reload
import sys

from nose2.tools import such

from testdoubles.fakes import callables
from tests.common.compat import mock
from tests.common.layers import UnitTestsLayer

with such.A("Fake Function's initialization method") as it:
    it.uses(UnitTestsLayer)

    @it.should("raise a TypeError when the provided live object is not callable")
    def test_should_raise_a_TypeError_when_the_provided_live_object_is_not_callable(case):
        with case.assertRaisesRegexp(TypeError, r"[a-zA-Z1-9_]* is not callable"):
            callables.FakeCallable(mock.NonCallableMagicMock())

    it.createTests(globals())

with such.A("Fake Function's live property") as it:
    it.uses(UnitTestsLayer)

    @it.has_test_setup
    def setup(case):
        case.old_callable = __builtins__['callable']
        __builtins__['callable'] = lambda c: True

    @it.has_test_teardown
    def teardown(case):
        __builtins__['callable'] = case.old_callable

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

with such.A("Fake Function's is instance method property") as it:
    it.uses(UnitTestsLayer)

    with it.having('a python 3.x runtime1'):
        @it.has_test_setup
        def setup(case):
            stubbed_sys = mock.MagicMock()
            stubbed_sys.version_info = (3, )

            case.patch_python_version = mock.patch.dict(sys.modules, sys=stubbed_sys)
            case.patch_python_version.start()

            reload(callables)

            case.old_callable = __builtins__['callable']
            __builtins__['callable'] = lambda c: True

        @it.has_test_teardown
        def teardown(case):
            case.patch_python_version.stop()

            reload(callables)

            __builtins__['callable'] = case.old_callable

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
            stubbed_sys = mock.MagicMock()
            stubbed_sys.version_info = (2, )

            case.patch_python_version = mock.patch.dict(sys.modules, sys=stubbed_sys)
            case.patch_python_version.start()

            reload(callables)

            case.old_callable = __builtins__['callable']
            __builtins__['callable'] = lambda c: True

        @it.has_test_teardown
        def teardown(case):
            case.patch_python_version.stop()

            reload(callables)

            __builtins__['callable'] = case.old_callable

        @it.should("return true if the live function is an instance method")
        def test_should_return_true_if_the_live_function_is_an_instance_method(case):
            sut = callables.FakeCallable(mock.DEFAULT)

            with mock.patch('inspect.ismethod', return_value=True):
                with mock.patch('inspect.getargspec', return_value=([], )):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return true if the live function is an unbound instance method")
        def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
            mocked_callable = mock.MagicMock()
            self = mock.PropertyMock()
            self.return_value = False
            type(mocked_callable).__self__ = self
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
            stubbed_sys = mock.MagicMock()
            stubbed_sys.version_info = (3, )

            case.patch_python_version = mock.patch.dict(sys.modules, sys=stubbed_sys)
            case.patch_python_version.start()

            reload(callables)

            case.old_callable = __builtins__['callable']
            __builtins__['callable'] = lambda c: True

        @it.has_test_teardown
        def teardown(case):
            case.patch_python_version.stop()

            reload(callables)

            __builtins__['callable'] = case.old_callable

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
            mocked_callable = mock.MagicMock()
            self = mock.PropertyMock()
            type(mocked_callable).__self__ = self

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=False):
                with mock.patch('inspect.getargspec'):
                    _ = sut.is_unbound_instance_method
                    self.assert_has_calls([])

    with it.having('a python 2.x runtime'):
        @it.has_test_setup
        def setup(case):
            stubbed_sys = mock.MagicMock()
            stubbed_sys.version_info = (2, )

            case.patch_python_version = mock.patch.dict(sys.modules, sys=stubbed_sys)
            case.patch_python_version.start()

            reload(callables)

            case.old_callable = __builtins__['callable']
            __builtins__['callable'] = lambda c: True

        @it.has_test_teardown
        def teardown(case):
            case.patch_python_version.stop()

            reload(callables)

            __builtins__['callable'] = case.old_callable

        @it.should("return true if the live function is an unbound instance method")
        def test_should_return_true_if_the_live_function_is_an_unbound_instance_method(case):
            mocked_callable = mock.MagicMock()
            self = mock.PropertyMock()
            self.return_value = False
            type(mocked_callable).__self__ = self
            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=True):
                    actual = sut.is_instance_method

            case.assertTrue(actual)

        @it.should("return false if the live function is a bound instance method")
        def test_should_return_false_if_the_live_function_is_a_bound_instance_method(case):
            mocked_callable = mock.MagicMock()
            self = mock.PropertyMock()
            self.return_value = True
            type(mocked_callable).__self__ = self
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
            mocked_callable = mock.MagicMock()
            self = mock.PropertyMock()
            self.return_value = False
            type(mocked_callable).__self__ = self

            sut = callables.FakeCallable(mocked_callable)

            with mock.patch('inspect.ismethod', return_value=True):
                    _ = sut.is_unbound_instance_method
                    self.assert_called_once_with()

    it.createTests(globals())