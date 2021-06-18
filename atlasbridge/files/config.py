from ruamel.yaml import YAML
from pathlib import Path
from typing import Dict, Any, Union, TextIO


def import_config(path: Union[Path, TextIO]) -> Dict[str, Any]:
    yaml = YAML(typ="safe")
    yaml.allow_unicode = True
    config = yaml.load(path)
    if config is None:
        config = {}
    return config


def write_config(conf: Dict[str, Any], path: Union[Path, TextIO]) -> None:
    yaml = YAML()
    yaml.allow_unicode = True
    yaml.dump(conf, path)
