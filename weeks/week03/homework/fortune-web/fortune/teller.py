"""The FortuneTeller — a stateful **callable** object (requirement #3).

Implements ``__call__`` (notes §1.5) so an instance can be invoked like a
function while keeping state between calls (a history of readings). Before
invoking each registered reading it guards with the built-in ``callable()``
(notes §1.4).
"""

from __future__ import annotations

from .decorators import Reading, registered_readings


class FortuneTeller:
    """Invoke like a function: ``teller(profile)`` → list of (label, value)."""

    def __init__(self, readings: tuple[Reading, ...] | None = None) -> None:
        # Default to the registry snapshot, but allow injection for testing.
        self._readings = readings if readings is not None else registered_readings()
        self.history: list[dict[str, object]] = []  # state kept between calls

    def __call__(self, profile: dict[str, object]) -> list[tuple[str, str]]:
        """Run every registered reading against the profile."""
        results: list[tuple[str, str]] = []
        for reading in self._readings:
            if not callable(reading):  # §1.4 — defensive guard
                continue
            # dict unpacking at the call site: spread profile into **kwargs (#2/#4)
            label, value = reading(**profile)
            results.append((label, value))

        # Record an immutable snapshot of this consultation (no mutation in place).
        self.history = [*self.history, {"name": profile.get("name"), "results": results}]
        return results

    @property
    def consultations(self) -> int:
        """How many times this teller has been called."""
        return len(self.history)
