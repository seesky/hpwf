"""Utility helpers for hadmin views."""

from typing import Tuple, Any


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def get_pagination_params(request, page_default: int = 1, rows_default: int = 20) -> Tuple[int, int]:
    """Return pagination parameters as integers with safe fallbacks."""
    page_value = getattr(request, 'POST', {}).get('page', page_default)
    rows_value = getattr(request, 'POST', {}).get('rows', rows_default)

    return _to_int(page_value, page_default), _to_int(rows_value, rows_default)
