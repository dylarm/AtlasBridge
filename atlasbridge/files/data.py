import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


def __read_excel(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def __read_csv(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def __read_zip(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def load_database(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def load_grade_file(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass
