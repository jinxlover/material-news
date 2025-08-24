#!/usr/bin/env python3
"""
extract.py

Contains utilities for parsing raw feed text into structured headlines and
metrics. It implements very simple regular-expression based extraction rules
that capture action, numbers of killed and injured, and the nature of the
incident. A subjectivity filter prevents adjectives and adverbs from
appearing in generated headlines.
"""

from __future__ import annotations

import re
from typing import Optional

# Regular expressions for capturing common metrics
# Support both "4 killed" and "kills 4" styles as well as
# "7 injured" and "injures 7" phrasings.
KILLED = re.compile(
    r"(?:\b(\d+)\s+(?:people|civilians|workers|soldiers)?\s*killed\b|\bkills\s*(\d+)\s*(?:people|civilians|workers|soldiers)?)",
    re.IGNORECASE,
)
INJURED = re.compile(
    r"(?:\b(\d+)\s+injur(?:ed|ies)\b|\binjures\s*(\d+)\s*(?:people|civilians|workers|soldiers|others)?)",
    re.IGNORECASE,
)
MAGNITUDE = re.compile(r"m(?:agnitude)?\s*(\d+(?:\.\d+)?)", re.IGNORECASE)

SUBJECTIVE_TOKENS = {
    "massive",
    "brutal",
    "tragic",
    "shocking",
    "controversial",
    "heinous",
    "horrific",
    "devastating",
}

# Ordered list of key incident types to match for the verb phrase
INCIDENT_TYPES = [
    "airstrike",
    "explosion",
    "earthquake",
    "fire",
    "flood",
    "shooting",
    "attack",
    "derailment",
]


def headline_from(text: str) -> str:
    """Generate a simple, factual headline from a feed entry text.

    The function looks for keywords describing the type of incident and
    aggregates information about casualties. It returns a sentence like
    ``"Explosion; 3 killed; 4 injured."``. Unknown elements are omitted.

    :param text: Raw text to examine.
    :returns: A concise headline string.
    """
    s = text.lower()
    # Determine incident type
    incident: Optional[str] = None
    for t in INCIDENT_TYPES:
        if t in s:
            incident = t
            break
    # Default incident label
    if incident is None:
        incident = "incident"
    # Find metrics
    killed_match = KILLED.search(s)
    injured_match = INJURED.search(s)
    magnitude_match = MAGNITUDE.search(s) if incident == "earthquake" else None
    parts = []
    parts.append(incident.capitalize())
    if killed_match:
        num = killed_match.group(1) or killed_match.group(2)
        parts.append(f"{num} killed")
    if injured_match:
        num = injured_match.group(1) or injured_match.group(2)
        parts.append(f"{num} injured")
    if magnitude_match:
        parts.append(f"M{magnitude_match.group(1)}")
    return "; ".join(parts) + "."


def forbid_subjective(s: str) -> None:
    """Raise an error if subjective words are detected in the string.

    This helper is used to enforce neutral language in headlines. If any
    adjectives or adverbs from the SUBJECTIVE_TOKENS set appear in the
    lowercased string, a ValueError is raised. Callers can catch this
    exception and handle it accordingly.

    :param s: String to examine.
    :raises ValueError: If subjective tokens are found.
    """
    tokens = re.findall(r"[a-z']+", s.lower())
    extras = SUBJECTIVE_TOKENS.intersection(tokens)
    if extras:
        raise ValueError(f"Subjective tokens not allowed: {', '.join(sorted(extras))}")


if __name__ == '__main__':  # pragma: no cover
    # Example usage for manual testing
    sample = (
        "Massive explosion kills 5 and injures 10 at a chemical plant in Houston, Texas."
    )
    try:
        forbid_subjective(sample)
    except ValueError as e:
        print(f"Subjectivity detected: {e}")
    print(headline_from(sample))