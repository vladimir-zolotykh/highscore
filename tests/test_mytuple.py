#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest
from mytuple import Person


@pytest.fixture
def bob():
    return Person("Bob", 37, 28000)


def test_person_repr(bob):
    """>>> bob\n('Bob', 37, 28000)"""
    assert bob == ("Bob", 37, 28000)


def test_person_fields(bob):
    """>>> bob.name, bob.age, bob.salary\n('Bob', 37, 28000)"""
    assert bob.name == "Bob"
    assert bob.age == 37
    assert bob.salary == 28000


def test_person_wrong_arg_count():
    """
    >>> alice = Person("Alice", 16)
    Traceback (most recent call last):
        ...
    TypeError: <class '__main__.Person'> expect 3 arguments
    """
    with pytest.raises(TypeError, match=r"expect 3 arguments"):
        Person("Alice", 16)
