#!/usr/bin/env python3
"""
verify.py

Responsible for assigning confidence scores to events and reconciling
statistics across sources. In the initial implementation, we simply add
a default confidence field and propagate min/max values when necessary.
"""

from __future__ import annotations

from typing import List, Dict, Any


def assign_confidence(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Assign a naive confidence score to each event.

    For demonstration, events with at least two sources get 0.6 and others
    receive 0.4. Future implementations should incorporate a more
    sophisticated scoring scheme based on the number and credibility of
    sources, geolocation accuracy and agreement on metrics.

    :param events: List of event dictionaries. Each must have a ``sources`` key.
    :returns: The same list with an added ``confidence`` key per event.
    """
    for evt in events:
        n = len(evt.get("sources", []))
        evt["confidence"] = 0.6 if n >= 2 else 0.4
    return events


if __name__ == '__main__':  # pragma: no cover
    sample = [
        {"headline": "Explosion; 2 killed.", "sources": [
            {"name": "Reuters", "url": "http://example.com"},
            {"name": "AP", "url": "http://example.org"},
        ]},
        {"headline": "Fire; 1 injured.", "sources": [
            {"name": "BBC", "url": "http://example.net"}
        ]},
    ]
    print(assign_confidence(sample))