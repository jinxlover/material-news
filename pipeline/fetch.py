#!/usr/bin/env python3
"""
fetch.py

This script reads feed configurations from the ``sources/wires.yaml`` file and
performs HTTP requests to retrieve raw RSS/Atom feeds. It returns a list of
dictionaries containing the name of the source and the response body. The
parser logic is intentionally simple at this stage; extracting structured
events happens in ``extract.py``.

Usage::

    python pipeline/fetch.py

The results are printed as JSON to stdout. In a full pipeline this data
would be piped into downstream processing.
"""

from __future__ import annotations

import json
import sys
from typing import Dict, List

import requests
import yaml

DEFAULT_TIMEOUT = 10


def load_config(path: str) -> Dict[str, Dict[str, str]]:
    """Load a YAML configuration file containing feed URLs.

    :param path: Path to YAML file.
    :returns: A dictionary with sections such as ``feeds`` and ``hazards``.
    """
    with open(path, 'r', encoding='utf-8') as fh:
        return yaml.safe_load(fh) or {}


def fetch_feeds(section: str = 'feeds', config_path: str = 'sources/wires.yaml') -> List[Dict[str, str]]:
    """Fetch all feeds defined in the specified configuration section.

    :param section: Which top-level key of the YAML to use (``feeds`` or ``hazards``).
    :param config_path: Path to the YAML configuration.
    :returns: A list of dicts with keys ``source`` and ``content``.
    """
    cfg = load_config(config_path)
    urls = cfg.get(section, {})
    results: List[Dict[str, str]] = []
    for name, url in urls.items():
        try:
            resp = requests.get(url, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            results.append({"source": name, "content": resp.text})
        except Exception as exc:  # noqa: BLE001
            print(f"Error fetching {name} ({url}): {exc}", file=sys.stderr)
    return results


def main() -> None:
    """Entry point for CLI usage."""
    # Fetch both wire feeds and hazards for completeness
    feeds = fetch_feeds('feeds', 'sources/wires.yaml')
    # Additional hazard feeds (if defined)
    try:
        hazards = fetch_feeds('hazards', 'sources/hazards.yaml')
    except FileNotFoundError:
        hazards = []
    combined = feeds + hazards
    print(json.dumps(combined, indent=2))


if __name__ == '__main__':
    main()