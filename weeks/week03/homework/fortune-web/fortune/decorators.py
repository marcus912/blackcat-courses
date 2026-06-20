"""Decorators for the 算命 app.

Showcases requirement #5 (decorators) and #4 (*args/**kwargs):

- ``@fortune`` is a *registration decorator* (notes §4.6): applying it appends
  the reading to a module-level registry and returns the function unchanged, so
  the app never has to maintain a hand-written list of readings.
- ``@log_call`` is a *well-behaved* wrapper (notes §3.6): it uses
  ``*args, **kwargs`` so any call signature passes through, and
  ``functools.wraps`` so the wrapper keeps the wrapped function's ``__name__``
  and ``__doc__``.
"""

from __future__ import annotations

import functools
from typing import Callable

# A reading takes the unpacked profile as keyword args and returns a label+value.
Reading = Callable[..., tuple[str, str]]

# The registry the app reads from. Populated at import time by ``@fortune``.
_REGISTRY: list[Reading] = []


def fortune(label: str) -> Callable[[Reading], Reading]:
    """Decorator *factory* (notes §3.8): ``@fortune("生肖")`` registers a reading.

    Three nested layers — factory → decorator → (here we return the function
    unchanged rather than a wrapper, the registration-decorator pattern §4.6).
    The ``label`` is stashed on the function object so the app can display it.
    """

    def decorator(func: Reading) -> Reading:
        func.label = label  # type: ignore[attr-defined]
        _REGISTRY.append(func)
        return func  # returned unchanged — we only registered it

    return decorator


def registered_readings() -> tuple[Reading, ...]:
    """Return an immutable snapshot of the registry (never expose the list)."""
    return tuple(_REGISTRY)


def log_call(func: Callable) -> Callable:
    """Wrapper that records each call. Uses *args/**kwargs passthrough (§3.6)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1  # rebinding a function attribute, no nonlocal needed
        return func(*args, **kwargs)

    wrapper.calls = 0  # type: ignore[attr-defined]
    return wrapper
