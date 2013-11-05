#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import sys
from testdoubles.utils import are_argspecs_identical

python3 = sys.version_info[0] == 3


class CallableInternalAttributesBaseMixin(object):
    @property
    def __name__(self):
        if not self.is_instance_method and not inspect.isfunction(self.live):
            return self.live.__class__.__name__

        return self.live.__name__

    @property
    def __self__(self):
        try:
            return self.live.__self__
        except AttributeError:
            raise AttributeError("'function' object has no attribute '__self__'")

    @property
    def __func__(self):
        if not self.is_instance_method:
            raise AttributeError("'function' object has no attribute '__func__'")

        if self.is_unbound_instance_method:
            return None

        return self.fake.__func__

    @property
    def __code__(self):
        return self.fake.__code__

    def __getattribute__(self, item):
        if item == '__doc__':
            return self.live.__doc__
        
        return super(CallableInternalAttributesBaseMixin, self).__getattribute__(item)


if python3:
    class CallableIntrospectionMixin(object):
        @property
        def is_unbound_instance_method(self):
            try:
                args = inspect.getargspec(self.live)[0]
                return args[0] == 'self' and not inspect.ismethod(self.live)
            except IndexError:
                return False
            except TypeError:
                return False

        @property
        def is_instance_method(self):
            return inspect.ismethod(self.live) or self.is_unbound_instance_method

    class CallableInternalAttributesMixin(CallableInternalAttributesBaseMixin):
        pass
else:
    class CallableIntrospectionMixin(object):
        @property
        def is_unbound_instance_method(self):
            return inspect.ismethod(self.live) and not self.live.__self__

        @property
        def is_instance_method(self):
            return inspect.ismethod(self.live) or self.is_unbound_instance_method

    class CallableInternalAttributesMixin(CallableInternalAttributesBaseMixin):
        @property
        def im_self(self):
            return self.__self__

        @property
        def im_class(self):
            return self.__self__.__class__

        @property
        def func_code(self):
            return self.__code__

        @property
        def func_doc(self):
            return self.__doc__

        @property
        def func_name(self):
            return self.live.__name__


class FakeCallable(CallableIntrospectionMixin, CallableInternalAttributesMixin):
    def __init__(self, live, inspect_args=False):
        if not callable(live):
            try:
                raise TypeError('%s is not callable.' % live.__name__)
            except AttributeError:
                raise TypeError('The provided object is not callable.')

        self._live = live

        if inspect_args:
            if inspect.isbuiltin(self.live):
                raise ValueError('Cannot inspect arguments of a builtin live object.')

            if not are_argspecs_identical(self.live, self.fake):
                raise ValueError("The provided live object's arguments %s does not match %s" % (
                    inspect.getargspec(self.live), inspect.getargspec(self.fake)))


    @property
    def live(self):
        return self._live

    @property
    def fake(self):
        return self.__call__

    def __call__(self, *args, **kwargs):
        pass