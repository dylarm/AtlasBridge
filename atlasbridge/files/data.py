import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any

from atlasbridge.constants import READING_EXTENSIONS, EXP_EXT

logger = logging.getLogger(__name__)


def __check_extension(path: Path, conf: Dict[str, Any]) -> bool:
    logger.debug(f"Testing extension for {path.name}")
    return path.suffix in conf[EXP_EXT]


def __validate_extension(path: Path) -> bool:
    return path.suffix in READING_EXTENSIONS


def __read_excel(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def __read_csv(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def __read_zip(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def __read_file(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def load_database(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def load_grade_file(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass
