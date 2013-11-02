#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect


def get_keyword_arguments(argspec):
    return argspec.args[-len(argspec.defaults):] if argspec.defaults else []


def are_arguments_identical(argspec1, argspec2):
    kwargs1 = get_keyword_arguments(argspec1)
    kwargs2 = get_keyword_arguments(argspec2)

    arguments1 = set(argspec1.args) - set(kwargs1)
    arguments2 = set(argspec2.args) - set(kwargs2)

    if len(arguments1) == len(arguments2) and not (argspec1.varargs or argspec2.varargs):
        return True
    elif any(_ for _ in arguments1) and argspec2.varargs or any(_ for _ in arguments2) and argspec1.varargs:
        return True

    return False


def are_keyword_arguments_identical(argspec1, argspec2):
    kwargs1 = get_keyword_arguments(argspec1)
    kwargs2 = get_keyword_arguments(argspec2)

    if kwargs1 == kwargs2 and not (argspec1.keywords or argspec2.keywords):
        return True
    if any(_ for _ in kwargs1) and argspec2.keywords or any(_ for _ in kwargs2) and argspec1.keywords:
        return True

    return False


def are_argspecs_identical(callable1, callable2):
    argspec1 = inspect.getargspec(callable1)
    argspec2 = inspect.getargspec(callable2)

    if argspec1 == argspec2:
        return True
    else:
        return are_arguments_identical(argspec1, argspec2) and are_keyword_arguments_identical(argspec1, argspec2)

__all__ = ('are_argspecs_identical', )