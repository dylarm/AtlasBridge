import sys, os

from hypothesis import given, strategies as st

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
