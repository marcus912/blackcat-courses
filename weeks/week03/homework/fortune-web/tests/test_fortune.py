"""Unit tests for the 算命 package.

Run from the homework folder:  pytest
Covers the 5 required syntaxes plus validation and determinism.
"""

from __future__ import annotations

import pytest

from fortune import FortuneTeller, ProfileError, build_profile
from fortune.decorators import log_call, registered_readings
from fortune.readings import ZODIAC, zodiac


# ---- profile: iterable + dictionary unpacking (#1, #2) ---------------------

def test_build_profile_merges_over_defaults():
    profile = build_profile(name="小明", birthday="1998-08-08")
    assert profile["year"] == 1998
    assert profile["month"] == 8
    assert profile["day"] == 8
    assert profile["name"] == "小明"


def test_build_profile_star_unpacks_name():
    profile = build_profile(name="王小明", birthday="2000-01-01")
    assert profile["surname"] == "王"        # head of iterable unpacking
    assert profile["given_name"] == "小明"   # *given gathered the rest


def test_defaults_are_not_mutated():
    from fortune.profile import DEFAULTS

    before = dict(DEFAULTS)
    build_profile(name="測試", birthday="1990-05-05")
    assert DEFAULTS == before  # immutability — merge produced a new dict


@pytest.mark.parametrize("bad", ["", "1998/08/08", "1998-08", "1998-13-01", "abc-08-08"])
def test_build_profile_rejects_bad_birthday(bad):
    with pytest.raises(ProfileError):
        build_profile(name="小明", birthday=bad)


def test_build_profile_rejects_empty_name():
    with pytest.raises(ProfileError):
        build_profile(name="  ", birthday="1998-08-08")


# ---- decorators: registration (#5) + *args/**kwargs passthrough (#4) -------

def test_readings_are_registered():
    labels = {r.label for r in registered_readings()}
    assert {"生肖", "幸運數字", "幸運色", "今日宜"} <= labels


def test_registered_readings_returns_immutable_snapshot():
    snap = registered_readings()
    assert isinstance(snap, tuple)


def test_log_call_counts_and_preserves_signature():
    @log_call
    def greet(*args, **kwargs):
        """say hi"""
        return "hi"

    assert greet.__name__ == "greet"        # functools.wraps kept metadata
    assert greet.__doc__ == "say hi"
    greet("a", b=1)
    greet()
    assert greet.calls == 2                 # *args/**kwargs passed through fine


# ---- zodiac correctness -----------------------------------------------------

@pytest.mark.parametrize(
    "year,expected",
    [(2008, "鼠"), (2000, "龍"), (1998, "虎"), (2010, "虎")],
)
def test_zodiac(year, expected):
    label, value = zodiac(year=year)
    assert label == "生肖"
    assert value == expected
    assert value in ZODIAC


# ---- teller: stateful callable (#3) ----------------------------------------

def test_teller_is_callable_and_runs_all_readings():
    teller = FortuneTeller()
    assert callable(teller)
    profile = build_profile(name="小明", birthday="1998-08-08")
    results = teller(profile)
    labels = [label for label, _ in results]
    assert labels == ["生肖", "幸運數字", "幸運色", "今日宜"]


def test_teller_keeps_history_between_calls():
    teller = FortuneTeller()
    teller(build_profile(name="A", birthday="1990-01-01"))
    teller(build_profile(name="B", birthday="1991-02-02"))
    assert teller.consultations == 2
    assert teller.history[0]["name"] == "A"


def test_readings_are_deterministic():
    teller_a = FortuneTeller()
    teller_b = FortuneTeller()
    profile = build_profile(name="小華", birthday="1995-03-14")
    assert teller_a(profile) == teller_b(profile)
