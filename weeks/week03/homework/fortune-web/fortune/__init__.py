"""算命 — a tiny, deterministic fortune-teller built on first-class functions.

Importing this package triggers the ``@fortune`` registration decorators in
``readings`` (decorators run at *import time*, notes §3.2), populating the
registry that :class:`FortuneTeller` reads from.
"""

from . import readings  # noqa: F401  — import for its registration side effect
from .profile import ProfileError, build_profile
from .teller import FortuneTeller

__all__ = ["FortuneTeller", "build_profile", "ProfileError"]
