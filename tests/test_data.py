import sys, os

import pytest
from hypothesis import given, note, strategies as st
from pathlib import Path
from typing import List
from test_config import CHAR_CAT

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from atlasbridge.files import data


@given(
    ext=st.characters(whitelist_categories=CHAR_CAT),
    config=st.lists(st.characters(whitelist_categories=CHAR_CAT)),
)
def test_extension_check(ext: str, config: List[str]):
    t_dict = {"expected_extensions": config}
    t_file = Path("test_file." + ext)
    if ext not in config:
        ext_in_dict = data.__check_extension(path=t_file, conf=t_dict)
        note(f"Extension NOT in dict result: {ext_in_dict}")
        assert ext_in_dict is False
    else:
        ext_in_dict = data.__check_extension(path=t_file, conf=t_dict)
        note(f"Extension IS in dict result: {ext_in_dict}")
        assert ext_in_dict is True


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
