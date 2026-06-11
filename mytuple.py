#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, bases, clsdict):
        fields = clsdict.get("_fields", [])
        for n, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(n)))


class MyTuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls} expect {n} arguments")
        return super().__new__(args)


class Person(MyTuple):
    _fields = ["name", "age", "salary"]


if __name__ == "__main__":
    bob = Person("Bob", 37, 28000)
    print(bob)
