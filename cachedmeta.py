#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class CacheMeta(type):
    cache = defaultdict(defaultdict)

    def __call__(cls, *args):
        stamp = tuple(args)
        if cls not in type(cls).cache or stamp not in type(cls).cache[cls]:
            type(cls).cache[cls][stamp] = super().__call__(*args)
        return type(cls).cache[cls][stamp]


class Cached(metaclass=CacheMeta):
    pass


class Person(Cached):
    def __init__(self, name, age, salary):
        print(f"Initializing Person({name}, {age}, {salary})")
        self.name = name
        self.age = age
        self.salary = salary


if __name__ == "__main__":
    bob = Person("Bob", 37, 28000)
    Person("Bob", 38, 28000)
    bob = Person("Bob", 37, 28000)
