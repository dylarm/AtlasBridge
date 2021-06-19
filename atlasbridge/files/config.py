import logging
from ruamel.yaml import YAML
from pathlib import Path
from typing import Dict, Any, Union, TextIO

logger = logging.getLogger(__name__)


def import_config(path: Union[Path, TextIO]) -> Dict[str, Any]:
    logging.debug("Reading yaml config")
    yaml = YAML(typ="safe")
    yaml.allow_unicode = True
    config = yaml.load(path)
    logging.debug(f"Read config: {config}")
    if config is None:
        config = {}
    logger.info(f"Config: {config}")
    return config


def write_config(conf: Dict[str, Any], path: Union[Path, TextIO]) -> None:
    logger.debug(f"Writing config: {conf}")
    yaml = YAML()
    yaml.allow_unicode = True
    yaml.dump(conf, path)
    logger.info(f"Wrote config to {path}")
