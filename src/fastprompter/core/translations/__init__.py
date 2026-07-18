"""Translation package — secured multi-language system.

Usage:
    from fastprompter.core.translations import tr, set_language, get_language

    btn.setText(tr("Always on Top"))
    btn.setToolTip(tr("Keep window above all others", lang="FRA"))

Architecture:
    - _engine.py:   core lookup, registry, fallback
    - _container.py:secured validation, loading, external slot
    - _compat.py:   backward-compat shim for old API
    - en.py:        458 English source keys (master)
    - ru/est/ukr/fra/spa.py: language data

See RFC.md for "injection" protocol.
"""

from __future__ import annotations

from ._compat import current_lang, get_language, set_language, tr
from ._engine import available_langs, coverage_report, missing_keys, tr_fmt

__all__ = [
    "available_langs",
    "coverage_report",
    "current_lang",
    "get_language",
    "missing_keys",
    "set_language",
    "tr",
    "tr_fmt",
]
