#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
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

    @classmethod
    def from_file(cls, f) -> Header:
        return Header(*struct.unpack(cls.fmt, f.read(struct.calcsize(cls.fmt))))


@dataclass
class Player:
    name: str
    score: int
    level: int
    fmt: str = "<20sIH"

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.name.encode(), self.score, self.level)

    @classmethod
    def from_file(cls, f) -> Player:
        player = Player(*struct.unpack(cls.fmt, f.read(struct.calcsize(cls.fmt))))
        player.name = player.name.rstrip(b"\0").decode()
        return player


players = [
    Player(*args)
    for args in (
        ("Alice", 1000, 15),
        ("Bob", 800, 12),
        ("Carol", 700, 10),
    )
]


def make_header() -> Header:
    return Header(b"HSCR", 1, len(players))


def write_scores() -> None:
    with open("scores.dat", "wb") as f:
        # header = Header(b"HSCR", 1, len(players))
        header = make_header()
        f.write(header.pack())
        # f.write(struct.pack("<4sHH", b"HSCR", 1, len(players)))  # magic  # version
        # for name, score, level in players:
        for player in players:
            # f.write(struct.pack("<20sIH", name.encode(), score, level))
            # player = Player(name.encode(), score, level)
            f.write(player.pack())


def read_scores() -> tuple[Header, list[Player]]:
    with open("scores.dat", "rb") as f:
        header = Header.from_file(f)
        players: list[Player] = []
        for _ in range(header.num_players):
            players.append(Player.from_file(f))
        return header, players


if __name__ == "__main__":
    write_scores()
    assert (make_header(), players) == read_scores()
