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
                return args[0] == 'self'
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
    def __init__(self, live):
        self._live = live

    @property
    def live(self):
        return self._live