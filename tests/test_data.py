import sys, os

import pytest
from hypothesis import given, assume, strategies as st
from pathlib import Path

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from atlasbridge.files import data


def test_read_excel():
    assert True


def test_read_csv():
    assert True


def test_read_zip():
    assert True


# Will need to create mock in-memory files for testing purposes
# https://coderbook.com/@marcus/how-to-mock-and-unit-test-with-pandas/
def test_load_database():
    assert True


def test_load_grade_file():
    assert True
