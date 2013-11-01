#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect


def are_arguments_identical(argspec1, argspec2):
    if len(argspec1.args) == len(argspec2.args):
        return True
    elif any(_ for _ in argspec1.args) and argspec2.varargs or any(_ for _ in argspec2.args) and argspec1.varargs:
        return True

    return False


def are_keyword_arguments_identical(argspec1, argspec2):
    kwargs1 = argspec1.args[-len(argspec1.defaults):] if argspec1.defaults else []
    kwargs2 = argspec2.args[-len(argspec2.defaults):] if argspec2.defaults else []

    if any(_ for _ in kwargs1) and argspec2.keywords or any(_ for _ in kwargs2) and argspec1.keywords:
        return True


def are_argspecs_identical(callable1, callable2):
    argspec1 = inspect.getargspec(callable1)
    argspec2 = inspect.getargspec(callable2)

    if argspec1 == argspec2:
        return True
    else:
        return are_arguments_identical(argspec1, argspec2) and are_keyword_arguments_identical(argspec1, argspec2)

__all__ = ('are_argspecs_identical', )