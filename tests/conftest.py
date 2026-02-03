"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def test_schedule_csv(fixtures_dir):
    """Return path to valid test schedule CSV."""
    return fixtures_dir / "test_schedule.csv"


@pytest.fixture
def test_recurring_csv(fixtures_dir):
    """Return path to valid test recurring slots CSV."""
    return fixtures_dir / "test_recurring_slots.csv"
