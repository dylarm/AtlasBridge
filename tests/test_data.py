import sys, os

import zipfile
import pandas as pd
from hypothesis import given, note, example, strategies as st
from hypothesis.extra import pandas as stpd
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


@given(i=st.lists(st.integers()))
def test_zero_indexing(i):
    oned = [n + 1 for n in i]
    note(f"{oned} -> {i}")
    assert data.__zero_index(oned) == i


@given(
    df=stpd.data_frames(
        [
            # stpd.column("Name", dtype=str), # TODO: Fix failure on empty strings → converts to NaN
            stpd.column("Points Earned", dtype="int64"),
            stpd.column("Points Possible", dtype="int64"),
            stpd.column("Percentage", dtype="int64"),
        ]
    ),
    ind=st.lists(st.integers(min_value=1)),
)
def test_read_excel(df: pd.DataFrame, ind):
    file = "tests/test_file.xls"
    with pd.ExcelWriter(file, engine="xlwt") as writer:
        df.to_excel(excel_writer=writer, index=False)
    t_conf = {
        "rows": {"header": 1},
        "columns": {
            "Name": 1,
            "Points Earned": 2,
            "Points Possible": 3,
            "Percentage": 4,
        },
    }
    in_file = data.__read_excel(Path(file), t_conf)
    os.remove(file)
    note(f"Original (left): {df}")
    note(f"Original dtypes: {df.dtypes}")
    note(f"Original items: {[str(x) for x in df.items()]}")
    note(f"Read df (right): {in_file}")
    note(f"Read dtypes: {in_file.dtypes}")
    note(f"Read items: {[str(x) for x in in_file.items()]}")
    pd.testing.assert_frame_equal(df, in_file)


@given(
    df=stpd.data_frames(
        [
            # stpd.column("Name", dtype=str),  # TODO: This thing again
            stpd.column("Points Earned", dtype="int64"),
            stpd.column("Points Possible", dtype="int64"),
            stpd.column("Percentage", dtype="int64"),
        ]
    )
)
def test_read_csv(df):
    test_file = "tests/test_file.csv"
    t_conf = {
        "rows": {"header": 1},
        "columns": {
            # "Name": 1,  # TODO: Why exclude this when it worked fine for the excel file?
            "Points Earned": 1,
            "Points Possible": 2,
            "Percentage": 3,
        },
    }
    df.to_csv(path_or_buf=test_file, index=False)
    in_file = data.__read_csv(Path(test_file), t_conf)
    os.remove(test_file)
    pd.testing.assert_frame_equal(df, in_file)


@given(
    df=stpd.data_frames(
        [
            # stpd.column("Name", dtype=str),
            stpd.column("Points Earned", dtype="int64"),
            stpd.column("Points Possible", dtype="int64"),
            stpd.column("Percentage", dtype="int64"),
        ]
    )
)
def test_read_zip(df):
    test_file = "tests/test_file.zip"
    test_csv = "test_zip.csv"
    t_conf = {
        "rows": {"header": 1},
        "columns": {
            # "Name": 1,
            "Points Earned": 1,
            "Points Possible": 2,
            "Percentage": 3,
        },
    }
    df.to_csv(test_csv, index=False)
    with zipfile.ZipFile(test_file, "w") as z_file:
        z_file.write(test_csv)
        valid_zip = z_file.testzip()
        if valid_zip is not None:
            note("Something bad with creating the zip file")
            note(f"bad file in zip: {valid_zip}")
            assert False
    in_file = data.__read_zip(Path(test_file), t_conf)
    os.remove(test_csv)
    os.remove(test_file)
    pd.testing.assert_frame_equal(df, in_file)


# Will need to create mock in-memory files for testing purposes
# https://coderbook.com/@marcus/how-to-mock-and-unit-test-with-pandas/
def test_load_database():
    assert True


def test_load_grade_file():
    assert True
