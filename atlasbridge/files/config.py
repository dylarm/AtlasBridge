from ruamel.yaml import YAML
from pathlib import Path
from . import AttrDict


def import_config(path: Path) -> AttrDict:
    yaml = YAML(typ='safe')
    config = AttrDict(yaml.load(path))
    return config


def write_config(conf: AttrDict) -> None:
    pass
