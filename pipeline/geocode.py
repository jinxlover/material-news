#!/usr/bin/env python3
"""
geocode.py

Provides a thin wrapper around a geocoding service. For privacy and rate
limiting reasons, this module caches results in-memory. A real
implementation might persist the cache to disk. Here we implement a stub
that always returns ``None`` coordinates but preserves the API shape.
"""

from __future__ import annotations

from typing import Dict, Optional

# Simple in-memory cache for demonstration purposes
_cache: Dict[str, Dict[str, Optional[str]]] = {}


def geocode_location(name: str) -> Dict[str, Optional[str]]:
    """Return geocoding information for a place name.

    In a production system this would call an external service (e.g.,
    OpenStreetMap Nominatim or Google Maps) and cache results. Here we
    stub it out to return ``None`` coordinates and placeholders.

    :param name: A human-readable location string like ``"Paris, France"``.
    :returns: A dictionary with keys ``lat``, ``lon``, ``iso2`` and ``admin1``.
    """
    if name in _cache:
        return _cache[name]
    # Placeholder result
    result: Dict[str, Optional[str]] = {
        "lat": None,
        "lon": None,
        "iso2": None,
        "admin1": None,
    }
    _cache[name] = result
    return result


if __name__ == '__main__':  # pragma: no cover
    print(geocode_location("Gaza City, Gaza"))