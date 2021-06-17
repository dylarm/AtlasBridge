from ruamel.yaml import YAML
from pathlib import Path
from typing import Dict, Any


def import_config(path: Path) -> Dict[str, Any]:
    yaml = YAML(typ="safe")
    config = yaml.load(path)
    return config


def write_config(conf: Dict[str, Any], path: Path) -> None:
    yaml = YAML()
    yaml.dump(conf, path)
