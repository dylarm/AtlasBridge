import sys, os

import pytest
from hypothesis import given, note, example, strategies as st
from pathlib import Path
from typing import List
from test_config import CHAR_CAT

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from atlasbridge.files import data
from atlasbridge.constants import EXP_EXT


@given(
    ext=st.characters(whitelist_categories=CHAR_CAT),
    config=st.lists(st.characters(whitelist_categories=CHAR_CAT)),
)
@example(ext="csv", config=["csv", "xls"])
@example(ext="zip", config=["csv", "xls"])
def test_extension_check(ext: str, config: List[str]):
    t_dict = {EXP_EXT: ["." + f for f in config]}
    t_file = Path("test_file." + ext)
    if ext in config:
        ext_in_dict = data.__check_extension(path=t_file, conf=t_dict)
        note(f"Extension IS in dict result: {ext_in_dict}")
        assert ext_in_dict
    else:
        ext_in_dict = data.__check_extension(path=t_file, conf=t_dict)
        note(f"Extension is NOT in dict result: {ext_in_dict}")
        assert ext_in_dict is False


@given(ext=st.text(min_size=1))
def test_invalidate_ext(ext: str):
    ext_path = Path("test_file." + ext)
    res = data.__validate_extension(ext_path)
    assert not res


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
