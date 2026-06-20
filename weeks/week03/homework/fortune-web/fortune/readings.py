"""The individual fortune readings.

Each reading is a plain function registered via ``@fortune(label)`` (#5) and
takes the unpacked profile as ``**kwargs`` (#4). They are deterministic: a
reading is a pure function of the profile, seeded by name+birthday, so no RNG.
"""

from __future__ import annotations

from .decorators import fortune, log_call

# 生肖 cycle. (year - 4) % 12 indexes this list (鼠 starts the cycle).
ZODIAC = ("鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬")

LUCKY_COLORS = ("赤紅", "金黃", "翠綠", "靛藍", "雪白", "墨黑", "緋紫")

BLESSINGS = (
    "今日諸事順遂，宜大膽前行。",
    "貴人就在身邊，記得開口求助。",
    "財氣漸旺，留心意外之喜。",
    "宜靜不宜動，沉住氣便是贏。",
    "桃花朵朵開，笑容是你的護身符。",
    "靈感如泉湧，動手做就對了。",
    "守得雲開見月明，再忍一忍。",
)


def _seed(name: str, year: int, month: int, day: int) -> int:
    """Stable, library-free hash of the profile → a non-negative int."""
    raw = f"{name}-{year:04d}-{month:02d}-{day:02d}"
    total = 0
    for ch in raw:
        total = (total * 31 + ord(ch)) % 1_000_003  # small prime, keeps it bounded
    return total


@fortune("生肖")
@log_call
def zodiac(**profile) -> tuple[str, str]:
    """Chinese zodiac from birth year."""
    year = profile["year"]
    return "生肖", ZODIAC[(year - 4) % 12]


@fortune("幸運數字")
@log_call
def lucky_number(**profile) -> tuple[str, str]:
    """A 1–9 lucky number derived from the seed."""
    seed = _seed(profile["name"], profile["year"], profile["month"], profile["day"])
    return "幸運數字", str(seed % 9 + 1)


@fortune("幸運色")
@log_call
def lucky_color(**profile) -> tuple[str, str]:
    """A lucky color picked deterministically from the seed."""
    seed = _seed(profile["name"], profile["year"], profile["month"], profile["day"])
    return "幸運色", LUCKY_COLORS[seed % len(LUCKY_COLORS)]


@fortune("今日宜")
@log_call
def daily_blessing(**profile) -> tuple[str, str]:
    """The day's blessing — rotates with month+day so it 'changes daily'."""
    seed = _seed(profile["name"], profile["year"], profile["month"], profile["day"])
    idx = (seed + profile["month"] * 31 + profile["day"]) % len(BLESSINGS)
    return "今日宜", BLESSINGS[idx]
