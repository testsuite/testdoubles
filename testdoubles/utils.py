#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from types import MethodType
from funcsigs import signature


def bind_function_to_object(f, obj):
    if 'self' not in signature(f).parameters.keys():
        raise ValueError('%s does not have a self argument' % f)

    setattr(obj, f.__name__, MethodType(f, None, obj))

    return obj


def not_implemented(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        raise NotImplementedError('%s is not implemented' % f)

    return wrapper