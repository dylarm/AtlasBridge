import sys, os

import pytest
from hypothesis import given, assume, strategies as st
from pathlib import Path

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from atlasbridge.files import config

CHAR_CAT = ("Lu", "Ll", "Lt", "Lm")


@given(
    c=st.dictionaries(
        keys=st.characters(whitelist_categories=CHAR_CAT),
        values=st.one_of(
            st.integers(min_value=0), st.characters(whitelist_categories=CHAR_CAT)
        ),
    )
)
def test_config_import_export(c):
    file = "tests/tmp.yml"
    tmp_file = open(file, "w", encoding="utf-8")
    config.write_config(conf=c, path=tmp_file)
    tmp_file.close()
    tmp_file = open(file, "r", encoding="utf-8")
    in_dict = config.import_config(path=tmp_file)
    tmp_file.close()
    os.remove(file)
    assert in_dict == c


def test_config_file_validity(dne):
    config_dir = Path("data/config")
    config_files = config_dir.glob("*.yml")
    only_required = ["db.yml"]  # Only test required fields
    req_fields = ["expected_extensions", "rows", "columns"]
    other_fields = ["contains_multiple", "needs_matching", "match_with"]
    column_fields = ["name", "name_pattern", "ID", "username"]
    for file in config_files:
        file_data = config.import_config(path=file)
        for field in req_fields:
            assert field in file_data
        for column in column_fields:
            assert column in file_data["columns"]
        if file.name not in only_required:
            for field in other_fields:
                assert field in file_data
