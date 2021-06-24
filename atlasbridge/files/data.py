import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Hashable

from atlasbridge.constants import READING_EXTENSIONS
from atlasbridge.constants import EXP_EXT, HEADER, ROW, COLUMN

logger = logging.getLogger(__name__)


def __check_extension(path: Path, conf: Dict[str, Any]) -> bool:
    logger.debug(f"Testing extension for {path.name}")
    return path.suffix in conf[EXP_EXT]


def __validate_extension(path: Path) -> bool:
    return path.suffix in READING_EXTENSIONS


def __zero_index(indices: List[int]) -> List[int]:
    """Subtract 1 from every value"""
    return [i - 1 for i in indices if i is not None]


def __correct_df_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Attempt to correct the dtype of a pandas dataframe based on heuristics"""
    logger.info(f"Checking dtypes for dataframe")
    new_dtypes: Dict[Hashable, str] = {}
    for column, data in df.items():
        logger.debug(f"Checking column {column}: {data.dtype}")
        col_name = str(column).lower()
        if (
            "points" in col_name or "percent" in col_name
        ) and not pd.api.types.is_numeric_dtype(data):
            logger.debug(f"{column} is not numeric, adding to fix dict")
            new_dtypes[column] = "int64"
        elif "name" in col_name and not pd.api.types.is_string_dtype(data):
            logger.debug(f"{column} is not string-like, adding to fix dict")
            new_dtypes[column] = "object"
    return df.astype(new_dtypes)


def __read_excel(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    """Read an Excel file, return a pandas DataFrame"""
    logger.info("Reading Excel file")
    # Columns are 0-indexed, but the YAML files are 1-indexed
    columns = __zero_index(conf[COLUMN].values())
    try:
        logger.debug(f"Attempting to load {path.name} with columns {columns}")
        excel_file = pd.read_excel(
            io=path,
            header=conf[ROW][HEADER] - 1,
            usecols=columns,
        )
        excel_file.index = pd.RangeIndex(start=0, stop=len(excel_file.index))
    except ValueError as e:
        excel_file = pd.DataFrame()
        logger.error(f"Error loading {path.name}: {e}")
    return __correct_df_dtypes(excel_file)


def __read_csv(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def __read_zip(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def __read_file(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    ext_expected = __check_extension(path, conf)
    extension = path.suffix
    if ext_expected:
        logger.info(f"Extension {extension} was expected for {path.name}")
    else:
        logger.warning(
            f"Extension {extension} was NOT expected for {path.name}"
            f"Expected one of: {conf['expected_extensions']}"
        )
    if extension in READING_EXTENSIONS[0]:  # csv
        db = __read_csv(path, conf)
    elif extension in READING_EXTENSIONS[1:3]:  # Excel, slice for position 1 and 2
        db = __read_excel(path, conf)
    elif extension in READING_EXTENSIONS[3]:  # zip
        db = __read_zip(path, conf)
    else:
        logger.error(f"No reader found for {extension} !")
        db = pd.DataFrame()
    return db


def load_database(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def load_grade_file(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass
