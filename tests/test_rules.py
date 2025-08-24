"""
Unit tests for pipeline.extract helper functions. These tests enforce
subjective language restrictions and validate the headline generator.
Run them with ``pytest``.
"""

from __future__ import annotations

import pytest

# Add the repository root to sys.path to allow importing pipeline modules
import sys
from pathlib import Path

# Ensure that the parent directory (repository root) is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.extract import forbid_subjective, headline_from


def test_forbid_subjective_allows_neutral():
    # Should not raise for neutral wording
    forbid_subjective("Explosion kills 3 and injures 2.")


def test_forbid_subjective_raises_on_subjective():
    with pytest.raises(ValueError):
        forbid_subjective("Massive explosion kills many.")


def test_headline_from_extraction():
    # Lowercase input is tested; ensure correct parts are found
    text = "Explosion in factory kills 4 workers and injures 7 others"
    headline = headline_from(text)
    assert headline == "Explosion; 4 killed; 7 injured."