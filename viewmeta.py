#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import BinaryIO, Self
import io
import struct


class Field:
    def __init__(self, name: str, offset: int):
        self._name = name
        self.offset = offset


class FieldStr(Field):
    def __init__(self, name: str, offset: int, fmt: str):
        super().__init__(name, offset)
        self.fmt = fmt

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        s = slice(self.offset, self.offset + struct.calcsize(self.fmt))
        t = struct.unpack_from(self.fmt, instance.view[s])
        assert len(t) == 1
        return t[0].rstrip(b"\0").decode() if self.fmt[-1] == "s" else t[0]


class FieldType(Field):
    def __init__(self, name: str, offset: int, factory: type):
        super().__init__(name, offset)
        self.factory = factory

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        s = slice(self.offset, self.offset + instance.view_size)
        return self.factory(instance.view[s])


class ViewMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        dcopy = dict(clsdict)
        offset = 0
        fields = []
        for k, v in clsdict.items():
            if k[:2] == "__" and k[-2:] == "__":
                continue
            if isinstance(v, str):
                dcopy[k] = FieldStr(k, offset, v)
                fields.append(k)
                offset += struct.calcsize(v)
            elif isinstance(v, ViewMeta):
                dcopy[k] = FieldType(k, offset, v)
                fields.append(k)
                offset += v.view_size
            elif isinstance(v, tuple):
                factory, _range = v
                for i in _range:
                    new_k = f"{k}_{str(i)}"
                    dcopy[new_k] = FieldType(new_k, offset, factory)
                    fields.append(new_k)
                    offset += factory.view_size
            else:
                pass
        dcopy["view_size"] = offset
        dcopy["_fields"] = fields
        return super().__new__(mcls, clsname, bases, dcopy)


class View(metaclass=ViewMeta):
    def __init__(self, bytesdata: bytes):
        self.view = memoryview(bytesdata)

    @classmethod
    def from_file(cls, f: BinaryIO) -> Self:
        return cls(f.read(cls.view_size))


class Header(View):
    magic = "<4s"
    version = "<H"
    num_players = "<H"


class Player(View):
    name = "<20s"
    score = "<I"
    level = "<H"

    def __repr__(self):
        return f"Player({self.name}, {self.score}, {self.level})"


class ThreePlayers(View):
    player = (Player, range(3))


def as_csv(view) -> str:
    return ", ".join(f"{k}={getattr(view, k)}" for k in view._fields)


if __name__ == "__main__":
    with open("scores.dat", "rb") as f:
        header = Header.from_file(f)
        print(as_csv(header))
        _data = f.read()
        f1 = io.BytesIO(_data)
        f2 = io.BytesIO(_data)
        for _ in range(header.num_players):
            player = Player.from_file(f1)
            print(as_csv(player))
        players3 = ThreePlayers.from_file(f2)
        print(as_csv(players3))
