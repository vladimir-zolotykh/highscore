#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import struct


class Field:
    def __init__(self, name: str, offset: int):
        self._name = name
        self.offset = offset


class FieldStr:
    def __init__(self, name: str, offset: int, fmt: str):
        super().__init__(name, offset)
        self.fmt = fmt

    def __get__(self, instance, owner=None):
        if instance in None:
            return self
        t = struct.unpack_from(self.fmt, instance.view[self.offset])
        return t[0] if len(t) == 1 else t


class FieldType:
    def __init__(self, name: str, offset: int, typ: type):
        super().__init__(name, offset)
        self.typ = typ

    def __get__(self, instance, owner=None):
        if instance in None:
            return self
        a = self.offset
        z = a + instance.view_size
        return self.typ(instance.view[a:z])


class ViewMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        dcopy = dict(clsdict)
        offset = 0
        for k, v in clsdict.items():
            if k[:2] == "__" and k[-2:] == "__":
                pass
            if isinstance(v, str):
                dcopy[k] = FieldStr(k, offset, v)
                offset += struct.calcsize(v)
            else:
                dcopy[k] = FieldType(k, offset, v)
                offset += v.view_size
        dcopy["view_size"] = offset
        return super().__new__(mcls, clsname, bases, dcopy)


class View(metaclass=ViewMeta):
    def __init__(self, bytesdata: bytes):
        self.view = memoryview(bytesdata)


class Header(View):
    magic = "<4s"
    versopm = "H"
    num_players = "H"


class Player(View):
    name = "<20s"
    score = "I"
    level = "H"


if __name__ == "__main__":
    with open("score.bin", "rb") as f:
        header = Header(f.read(Header.view_size))
        print(header)
        for _ in range(header.num_players):
            player = Player.from_file(f)
            print(player)
