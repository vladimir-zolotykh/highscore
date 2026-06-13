# test_scores.py

import io
import struct

from viewmeta import (
    Header,
    Player,
    ThreePlayers,
    as_csv,
)


def make_player(name: str, score: int, level: int) -> bytes:
    return struct.pack(
        "<20sIH",
        name.encode(),
        score,
        level,
    )


def test_header_fields():
    data = struct.pack(
        "<4sHH",
        b"SCOR",
        2,
        3,
    )

    hdr = Header(data)

    assert hdr.magic == "SCOR"
    assert hdr.version == 2
    assert hdr.num_players == 3


def test_header_from_file():
    data = struct.pack(
        "<4sHH",
        b"GAME",
        1,
        5,
    )

    hdr = Header.from_file(io.BytesIO(data))

    assert hdr.magic == "GAME"
    assert hdr.version == 1
    assert hdr.num_players == 5


def test_player_fields():
    player = Player(
        make_player(
            "Alice",
            1000,
            42,
        )
    )

    assert player.name == "Alice"
    assert player.score == 1000
    assert player.level == 42


def test_player_repr():
    player = Player(
        make_player(
            "Bob",
            777,
            9,
        )
    )

    assert repr(player) == "Player(Bob, 777, 9)"


def test_player_from_file():
    data = make_player(
        "Charlie",
        500,
        7,
    )

    player = Player.from_file(io.BytesIO(data))

    assert player.name == "Charlie"
    assert player.score == 500
    assert player.level == 7


def test_as_csv_player():
    player = Player(
        make_player(
            "Dave",
            123,
            4,
        )
    )

    assert as_csv(player) == "name=Dave, score=123, level=4"


def test_view_sizes():
    assert Header.view_size == struct.calcsize("<4sHH")
    assert Player.view_size == struct.calcsize("<20sIH")
    assert ThreePlayers.view_size == 3 * Player.view_size


def test_threeplayers_metaclass_generated_fields():
    assert ThreePlayers._fields == [
        "player_0",
        "player_1",
        "player_2",
    ]

    assert hasattr(ThreePlayers, "player_0")
    assert hasattr(ThreePlayers, "player_1")
    assert hasattr(ThreePlayers, "player_2")


def test_threeplayers_parsing():
    data = b"".join(
        [
            make_player("Alice", 100, 1),
            make_player("Bob", 200, 2),
            make_player("Charlie", 300, 3),
        ]
    )

    players = ThreePlayers(data)

    assert players.player_0.name == "Alice"
    assert players.player_0.score == 100
    assert players.player_0.level == 1

    assert players.player_1.name == "Bob"
    assert players.player_1.score == 200
    assert players.player_1.level == 2

    assert players.player_2.name == "Charlie"
    assert players.player_2.score == 300
    assert players.player_2.level == 3


def test_threeplayers_from_file():
    data = b"".join(
        [
            make_player("P1", 10, 1),
            make_player("P2", 20, 2),
            make_player("P3", 30, 3),
        ]
    )

    players = ThreePlayers.from_file(io.BytesIO(data))

    assert players.player_0.name == "P1"
    assert players.player_1.name == "P2"
    assert players.player_2.name == "P3"


def test_as_csv_threeplayers():
    data = b"".join(
        [
            make_player("A", 1, 1),
            make_player("B", 2, 2),
            make_player("C", 3, 3),
        ]
    )

    players = ThreePlayers(data)

    csv = as_csv(players)

    assert "player_0=Player(A, 1, 1)" in csv
    assert "player_1=Player(B, 2, 2)" in csv
    assert "player_2=Player(C, 3, 3)" in csv
