"""
schema.py

Defines the JSON schema for events produced by the Material News pipeline.
The schema is provided as a plain Python dictionary; tools such as
jsonschema can be used to validate event dictionaries against this schema.
"""

from __future__ import annotations

from typing import Dict, Any


def event_schema() -> Dict[str, Any]:
    """Return the JSON schema describing a material news event."""
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Material News Event",
        "type": "object",
        "required": [
            "id",
            "event_type",
            "headline",
            "actors",
            "targets",
            "location",
            "when_utc",
            "metrics",
            "sources",
            "confidence",
            "updated_at",
            "method",
            "version",
        ],
        "properties": {
            "id": {"type": "string"},
            "event_type": {"type": "string"},
            "headline": {"type": "string"},
            "actors": {"type": "array", "items": {"type": "string"}},
            "targets": {"type": "array", "items": {"type": "string"}},
            "location": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "lat": {"type": ["number", "null"]},
                    "lon": {"type": ["number", "null"]},
                    "iso2": {"type": ["string", "null"]},
                    "admin1": {"type": ["string", "null"]},
                },
                "required": ["name"],
            },
            "when_utc": {"type": "string", "format": "date-time"},
            "metrics": {
                "type": "object",
                "properties": {
                    "killed": {"type": ["integer", "null"]},
                    "injured": {"type": ["integer", "null"]},
                    "magnitude": {"type": ["number", "null"]},
                    "area_burned_km2": {"type": ["number", "null"]},
                },
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "url": {"type": "string", "format": "uri"},
                        "first_seen": {"type": ["string", "null"], "format": "date-time"},
                    },
                    "required": ["name", "url"],
                },
            },
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "notes": {"type": ["string", "null"]},
            "updated_at": {"type": "string", "format": "date-time"},
            "method": {"type": "string"},
            "version": {"type": "integer"},
        },
    }


if __name__ == '__main__':  # pragma: no cover
    import json
    print(json.dumps(event_schema(), indent=2))