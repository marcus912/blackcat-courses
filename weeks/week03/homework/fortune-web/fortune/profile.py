"""Build a birth profile from raw form input.

Showcases requirement #1 (iterable unpacking) and #2 (dictionary unpacking).
Everything here is deterministic: a profile is a pure function of (name, birthday)
so both the web page and the tests are reproducible — no real RNG.
"""

from __future__ import annotations

# Defaults merged under any user input via dict unpacking (notes §1.7).
DEFAULTS: dict[str, object] = {
    "name": "無名氏",
    "year": 2000,
    "month": 1,
    "day": 1,
}


class ProfileError(ValueError):
    """Raised when form input fails validation (fail fast, clear message)."""


def _parse_birthday(birthday: str) -> tuple[int, int, int]:
    """Split ``YYYY-MM-DD`` using **iterable unpacking** (notes §1.6).

    Validates at the boundary — never trust external input.
    """
    parts = birthday.strip().split("-")
    if len(parts) != 3:
        raise ProfileError("生日格式須為 YYYY-MM-DD，例如 1998-08-08")
    try:
        # iterable unpacking: a 3-tuple straight into three names
        year, month, day = (int(p) for p in parts)
    except ValueError:
        raise ProfileError("生日的年月日必須都是數字")

    if not (1 <= month <= 12 and 1 <= day <= 31):
        raise ProfileError("月份須為 1–12、日期須為 1–31")
    return year, month, day


def build_profile(name: str, birthday: str) -> dict[str, object]:
    """Merge validated input over defaults via **dictionary unpacking** (§1.7)."""
    name = (name or "").strip()
    if not name:
        raise ProfileError("請輸入姓名")

    year, month, day = _parse_birthday(birthday)

    # Demonstrate star-unpacking too: keep the surname char, gather the rest.
    surname, *given = name
    given_name = "".join(given)

    overrides = {
        "name": name,
        "surname": surname,
        "given_name": given_name,
        "year": year,
        "month": month,
        "day": day,
    }
    # {**a, **b} — later keys win. The canonical dict-unpacking merge.
    return {**DEFAULTS, **overrides}
