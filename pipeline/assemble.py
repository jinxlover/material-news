#!/usr/bin/env python3
"""
assemble.py

Assemble the final event feed by combining data from extraction, geocoding,
deduplication and verification. The output is written to
``data/events.json``. In a real system, input would be piped from previous
pipeline steps. Here we build a simple, hard-coded example to illustrate
the format.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any


def build_sample_events() -> List[Dict[str, Any]]:
    """Return a list of example events for demonstration purposes."""
    return [
        {
            "id": "evt_2025-01-01T00:00:00Z_demo",
            "event_type": "explosion",
            "headline": "Explosion; 3 killed; 5 injured.",
            "actors": ["Unknown"],
            "targets": ["warehouse"],
            "location": {
                "name": "Example City, EX",
                "lat": None,
                "lon": None,
                "iso2": "EX",
                "admin1": None,
            },
            "when_utc": "2025-01-01T00:00:00Z",
            "metrics": {
                "killed": 3,
                "injured": 5,
                "magnitude": None,
                "area_burned_km2": None,
            },
            "sources": [
                {"name": "Reuters", "url": "http://example.com", "first_seen": "2025-01-01T01:00:00Z"},
                {"name": "AP", "url": "http://example.org", "first_seen": "2025-01-01T01:05:00Z"},
            ],
            "confidence": 0.6,
            "notes": "Sample event.",
            "updated_at": "2025-01-01T01:06:00Z",
            "method": "rule",
            "version": 1,
        }
    ]


def write_events(events: List[Dict[str, Any]], path: str = 'data/events.json') -> None:
    """Write events to a JSON file in UTF-8 encoding.

    :param events: List of event dictionaries.
    :param path: Destination file path relative to repository root.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(events, fh, ensure_ascii=False, indent=2)


def main() -> None:
    events = build_sample_events()
    write_events(events)
    print(f"Wrote {len(events)} event(s) to data/events.json")


if __name__ == '__main__':
    main()