#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
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


@dataclass
class Player:
    name: str
    score: int
    level: int
    fmt: str = "<20sIH"

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.name.encode(), self.score, self.level)


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
        magic, version, count = struct.unpack("<4sHH", f.read(8))
        header: Header = Header(magic, version, count)
        players: list[Player] = []
        for _ in range(count):
            name, score, level = struct.unpack("<20sIH", f.read(26))
            name = name.rstrip(b"\0").decode()
            players.append(Player(name, score, level))
        return header, players


if __name__ == "__main__":
    write_scores()
    _header, _players = read_scores()
    # _players = read_scores()[1]
    # print(players)
    # print(_players[1:])
    assert _header == make_header()
    assert players == _players
