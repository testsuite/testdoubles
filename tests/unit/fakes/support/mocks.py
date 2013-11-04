#!/usr/bin/env python
# -*- coding: utf-8 -*-
from testdoubles.fakes import callables


def mock_are_argspecs_identical(case, mocked_are_argspecs_identical):
    try:
        old_init_globals = callables.FakeCallable.__init__.__globals__
        callables.FakeCallable.__init__.__globals__['are_argspecs_identical'] = mocked_are_argspecs_identical
    except AttributeError:
        old_init_globals = callables.FakeCallable.__init__.func_globals
        callables.FakeCallable.__init__.func_globals['are_argspecs_identical'] = mocked_are_argspecs_identical
    case.old_init_globals = old_init_globals


def unmock_are_argspecs_identical(case):
    try:
        callables.FakeCallable.__init__.__globals__.update(case.old_init_globals)
    except AttributeError:
        callables.FakeCallable.__init__.func_globals.update(case.old_init_globals)