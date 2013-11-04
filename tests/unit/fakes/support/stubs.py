#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imp import reload
import sys
import mock
from testdoubles.fakes import callables


def stub_callable(case, return_value):
    try:
        case.old_callable = __builtins__['callable']
        __builtins__['callable'] = lambda c: return_value
    except TypeError:
        case.old_callable = __builtins__.callable
        __builtins__.callable = lambda c: return_value


def unstub_callable(case):
    try:
        __builtins__['callable'] = case.old_callable
    except TypeError:
        __builtins__.callable = case.old_callable


def stub_are_argspecs_identical(case, return_value):
    try:
        old_init_globals = callables.FakeCallable.__init__.__globals__
        callables.FakeCallable.__init__.__globals__['are_argspecs_identical'] = lambda _, __: return_value
    except AttributeError:
        old_init_globals = callables.FakeCallable.__init__.func_globals
        callables.FakeCallable.__init__.func_globals['are_argspecs_identical'] = lambda _, __: return_value
    case.old_init_globals = old_init_globals


def unstub_are_argspecs_identical(case):
    try:
        callables.FakeCallable.__init__.__globals__.update(case.old_init_globals)
    except AttributeError:
        callables.FakeCallable.__init__.func_globals.update(case.old_init_globals)


def stub_python_version(case, major_version):
    stubbed_sys = mock.MagicMock()
    stubbed_sys.version_info = (major_version, )
    case.patch_python_version = mock.patch.dict(sys.modules, sys=stubbed_sys)
    case.patch_python_version.start()
    reload(callables)


def unstub_python_version(case):
    case.patch_python_version.stop()
    reload(callables)