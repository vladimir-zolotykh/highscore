import io
import pytest

from player_records import (
    Header,
    Player,
    players,
    write_scores,
    read_scores,
)


def test_header_from_int():
    header = Header.from_int(3)

    assert header.magic == b"HSCR"
    assert header.version == 1
    assert header.num_players == 3


def test_header_roundtrip():
    header = Header(b"HSCR", 1, 42)

    buf = io.BytesIO()
    header.write(buf)

    buf.seek(0)

    restored = Header.from_file(buf)

    assert restored == header


def test_player_roundtrip():
    player = Player("Alice", 1000, 15)

    buf = io.BytesIO()
    player.write(buf)

    buf.seek(0)

    restored = Player.from_file(buf)

    assert restored == player


def test_player_name_padding_removed():
    player = Player("Bob", 800, 12)

    buf = io.BytesIO()
    player.write(buf)

    buf.seek(0)

    restored = Player.from_file(buf)

    assert restored.name == "Bob"
    assert restored.score == 800
    assert restored.level == 12


def test_multiple_players_roundtrip():
    buf = io.BytesIO()

    Header.from_int(len(players)).write(buf)

    for player in players:
        player.write(buf)

    buf.seek(0)

    header = Header.from_file(buf)
    restored = [Player.from_file(buf) for _ in range(header.num_players)]

    assert header == Header.from_int(len(players))
    assert restored == players


def test_write_read_scores(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    write_scores()

    header, restored_players = read_scores()

    assert header == Header.from_int(len(players))
    assert restored_players == players


def test_scores_file_created(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    write_scores()

    assert (tmp_path / "scores.dat").exists()


def test_header_read_returns_correct_size():
    buf = io.BytesIO(Header.from_int(1).pack())

    data = Header.read(buf)

    assert len(data) == Header.pack(Header.from_int(1)).__len__()
