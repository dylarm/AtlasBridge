import logging
import pandas as pd
from pathlib import Path
from zipfile import ZipFile
from typing import Dict, List, Any, Hashable, Union, IO

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


def __read_excel(path: Union[Path, IO], conf: Dict[str, Any]) -> pd.DataFrame:
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


def __read_csv(path: Union[Path, IO], conf: Dict[str, Any]) -> pd.DataFrame:
    """Read a CSV, return a pandas DataFrame"""
    logger.info("Reading CSV file")
    columns = __zero_index(conf[COLUMN].values())
    try:
        logger.debug(f"Attempting to load {path.name} with columns {columns}")
        csv_file = pd.read_csv(
            filepath_or_buffer=path,
            sep=",",  # Better to be explicit than implicit
            header=conf[ROW][HEADER] - 1,
            usecols=columns,
        )
        csv_file.index = pd.RangeIndex(start=0, stop=len(csv_file.index))
    except ValueError as e:
        csv_file = pd.DataFrame()
        logger.error(f"Error loading {path.name}: {e}")
    return __correct_df_dtypes(csv_file)


def __read_zip(path: Union[Path, IO], conf: Dict[str, Any]) -> pd.DataFrame:
    """Open a zip file to find a csv/xls(x), then read that and return a pandas DataFrame"""
    logger.debug("Loading zip file")
    with ZipFile(path) as zfile:
        zlist = zfile.namelist()
        znames = enumerate(zlist)  # We'll need this for the list comps
        logger.debug(f"Files in archive: {zlist}")
        potential_files = []
        for extension in READING_EXTENSIONS:
            potential_files += [i for i, n in znames if extension in n]
            # This may allow for recursion, i.e. a zip within a zip. We can go all the way down to figure out where
            # a valid csv/excel file may be. Also a possible vector of attack, I suppose, if someone wanted to be mean
            # and put in a zip-bomb instead...
        logger.debug(f"Potential file indices: {potential_files}")
        if not potential_files:
            logger.error("No valid files found in zip file")
            zip_file = pd.DataFrame()
            return zip_file
        elif len(potential_files) > 1:
            logger.warning(
                f"More than 1 valid file found: {len(potential_files)}"
                f"Defaulting to the first one: {zlist[potential_files[0]]}"
            )
        file_to_use = zlist[potential_files[0]]
        logger.info(f"Extracting '{file_to_use}'")
        with zfile.open(file_to_use) as file:
            zip_file = __load_file(file=file, conf=conf, ext=Path(file_to_use).suffix)
        return zip_file  # No need to run __correct_df_dtypes() since it's been run by now if needed


def __load_file(file: Union[Path, IO], conf: Dict[str, Any], ext: str = "") -> pd.DataFrame:
    logger.debug("Start loading file")
    if isinstance(file, Path) and not ext:
        ext = file.suffix
    if ext in READING_EXTENSIONS[0]:  # csv
        db = __read_csv(file, conf)
    elif ext in READING_EXTENSIONS[1:3]:  # Excel, slice for position 1 and 2
        db = __read_excel(file, conf)
    elif ext in READING_EXTENSIONS[3]:  # zip
        db = __read_zip(file, conf)
    else:
        logger.error(f"No reader found for {ext} !")
        db = pd.DataFrame()
    return db


def __read_file(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    ext_expected = __check_extension(path, conf)
    extension = path.suffix
    if ext_expected:
        logger.info(f"Extension {extension} was expected for {path.name}")
    else:
        logger.warning(
            f"Extension {extension} was NOT expected for {path.name}"
            f"Expected one of: {conf[EXP_EXT]}"
        )
    db = __load_file(file=path, conf=conf, ext=extension)
    return db


def load_database(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass


def load_grade_file(path: Path, conf: Dict[str, Any]) -> pd.DataFrame:
    pass
