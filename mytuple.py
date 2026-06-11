#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> bob = Person("Bob", 37, 28000)
>>> bob
('Bob', 37, 28000)
>>> bob.name, bob.age, bob.salary
('Bob', 37, 28000)
>>> alice = Person("Alice", 16)
Traceback (most recent call last):
...
TypeError: <class '__main__.Person'> expect 3 arguments
>>>
"""
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        fields = clsdict.get("_fields", [])
        for n, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(n)))


class MyTuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls} expect {n} arguments")
        return super().__new__(cls, args)


class Person(MyTuple):
    _fields = ["name", "age", "salary"]


if __name__ == "__main__":

    # bob = Person("Bob", 37, 28000)
    # print(bob)
    import doctest

    doctest.testmod()
