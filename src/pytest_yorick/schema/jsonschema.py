from typing import Mapping

import fastjsonschema

from pytest_yorick.exceptions import BadSchemaError


def verify_jsonschema(to_verify: Mapping, schema: Mapping) -> None:
    point_validator = fastjsonschema.compile(schema)
    point_validator(to_verify)
