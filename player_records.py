#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Any
from dataclasses import dataclass
import struct


@dataclass
class Header:
    magic: str
    version: int
    num_players: int
    fmt: str = "<4sHH"

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.magic, self.version, self.num_players)

    def write(self, f):
        f.write(self.pack())

    @classmethod
    def from_file(cls, f) -> Header:
        return Header(*struct.unpack(cls.fmt, cls.read(f)))

    @classmethod
    def read(cls, f) -> bytes:
        return f.read(struct.calcsize(cls.fmt))

    @classmethod
    def from_int(cls, count) -> Header:
        return Header(b"HSCR", 1, count)


@dataclass
class Player:
    name: str
    score: int
    level: int
    fmt: str = "<20sIH"

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.name.encode(), self.score, self.level)

    def write(self, f):
        f.write(self.pack())

    @classmethod
    def unpack(cls, f) -> tuple[Any, ...]:
        tup = struct.unpack(cls.fmt, f.read(struct.calcsize(cls.fmt)))
        return tuple((tup[0].rstrip(b"\0").decode(), *tup[1:]))

    @classmethod
    def from_file(cls, f) -> Player:
        player = Player(*cls.unpack(f))
        return player


players = [
    Player(*args)
    for args in (
        ("Alice", 1000, 15),
        ("Bob", 800, 12),
        ("Carol", 700, 10),
    )
]


def write_scores() -> None:
    with open("scores.dat", "wb") as f:
        Header.from_int(len(players)).write(f)
        for player in players:
            player.write(f)


def read_scores() -> tuple[Header, list[Player]]:
    with open("scores.dat", "rb") as f:
        header = Header.from_file(f)
        players: list[Player] = [Player.from_file(f) for _ in range(header.num_players)]
        return header, players


if __name__ == "__main__":
    write_scores()
    assert (Header.from_int(len(players)), players) == read_scores()
