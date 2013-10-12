#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import sys

python3 = sys.version_info[0] == 3

if python3:
    class CallableIntrospectionMixin(object):
        @property
        def is_unbound_instance_method(self):
            try:
                args = inspect.getargspec(self.live)[0]
                return args[0] == 'self' and not inspect.ismethod(self.live)
            except IndexError:
                return False

        @property
        def is_instance_method(self):
            return inspect.ismethod(self.live) or self.is_unbound_instance_method
else:
    class CallableIntrospectionMixin(object):
        @property
        def is_unbound_instance_method(self):
            return inspect.ismethod(self.live) and not self.live.__self__

        @property
        def is_instance_method(self):
            return inspect.ismethod(self.live) or self.is_unbound_instance_method

class FakeCallable(CallableIntrospectionMixin):
    def __init__(self, live, inspect_args=False):
        if not callable(live):
            try:
                raise TypeError('%s is not callable.' % live.__name__)
            except AttributeError:
                raise TypeError('The provided object is not callable.')

        if inspect_args:
            live_args_spec = inspect.getargspec(live)
            fake_args_spec = inspect.getargspec(self.__call__)
            if live_args_spec != fake_args_spec:
                raise ValueError("The provided live object's arguments %s does not match %s" % (live_args_spec, fake_args_spec))

        self._live = live

    @property
    def live(self):
        return self._live

    @property
    def fake(self):
        return self.__call__

    def __call__(self, *args, **kwargs):
        pass