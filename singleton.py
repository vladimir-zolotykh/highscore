#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Singleton(type):
    _instances = set()

    def __call__(cls, *args, **kwds):
        if cls in type(cls)._instances:
            return cls
        else:
            new_cls = super().__call__(*args, **kwds)
            type(cls)._instances.add(new_cls)
            return new_cls


class Logger(metaclass=Singleton):
    def __init__(self):
        print(f"Initializing {self.__class__}")


class Module(metaclass=Singleton):
    def __init__(self):
        print(f"Initializing {self.__class__}")


if __name__ == "__main__":
    el1 = Logger()
    el2 = Logger()
    assert el1 is el2
    m1 = Module()
    m2 = Module()
    assert m1 is m2
