import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any

from atlasbridge.constants import READING_EXTENSIONS
from atlasbridge.constants import EXP_EXT, HEADER, ROW, COLUMN

logger = logging.getLogger(__name__)


def __check_extension(path: Path, conf: Dict[str, Any]) -> bool:
    logger.debug(f"Testing extension for {path.name}")
    return path.suffix in conf[EXP_EXT]


def __validate_extension(path: Path) -> bool:
    return path.suffix in READING_EXTENSIONS


def __read_excel(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    """Read an Excel file, return a pandas DataFrame"""
    # Columns are 0-indexed, but the YAML files are 1-indexed
    columns = [c - 1 for c in conf[COLUMN].values() if c is not None]
    try:
        excel_file = pd.read_excel(
            io=path,
            header=conf[ROW][HEADER],
            usecols=columns,
        )
    except ValueError as e:
        excel_file = pd.DataFrame()
        logger.error(f"Error loading {path.name}: {e}")
    return excel_file


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
    if extension is READING_EXTENSIONS[0]:  # csv
        db = __read_csv(path, conf)
    elif (
        extension is READING_EXTENSIONS[1] or extension is READING_EXTENSIONS[2]
    ):  # Excel
        db = __read_excel(path, conf)
    elif extension is READING_EXTENSIONS[3]:  # zip
        db = __read_zip(path, conf)
    else:
        logger.error(f"No reader found for {extension} !")
        db = pd.DataFrame()
    return db


def load_database(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def load_grade_file(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass
