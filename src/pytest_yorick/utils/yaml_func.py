import os
from typing import Union

import yaml
from box import Box
from yaml import parser

from pytest_yorick.exceptions import YamlException


def load_single_yaml(filename: Union[str, os.PathLike]) -> dict:
    with open(filename, encoding="utf-8") as file:
        try:
            raw: dict = yaml.safe_load(file)
        except Exception as e:
            raise YamlException(f"fail to load yamlfile: {e}") from e
    return raw


def dump_yaml(payload: dict):
    return yaml.safe_dump(payload, indent=4)


def represent_box(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data)


yaml.SafeDumper.add_representer(Box, represent_box)
