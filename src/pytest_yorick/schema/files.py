import os
from typing import Mapping, Dict

from pytest_yorick.schema.jsonschema import verify_jsonschema
from pytest_yorick.utils.yaml_func import load_single_yaml


class SchemaCache:
    """Caches loaded schemas"""

    def __init__(self) -> None:
        self._loaded: Dict[str, Dict] = {}

    def _load_base_schema(self, schema_filename):
        try:
            return self._loaded[schema_filename]
        except KeyError:
            self._loaded[schema_filename] = load_single_yaml(schema_filename)
            return self._loaded[schema_filename]

    def __call__(self, schema_filename: str):
        """Load the schema file and cache it for future use

        Args:
            schema_filename: filename of schema

        Returns:
            loaded schema
        """

        return self._load_base_schema(schema_filename)


load_schema_file = SchemaCache()


def verify_tests(test_spec: Mapping, is_main: bool) -> None:
    """Verify that a specific test block is correct

    Args:
        test_spec: Test in dictionary form
        is_main: Schema is for mainfile or subfile

    Raises:
        BadSchemaError: Schema did not match
    """

    here = os.path.dirname(os.path.abspath(__file__))
    if is_main:
        schema_filename = os.path.join(here, "tests.mainfile.yaml")
    else:
        schema_filename = os.path.join(here, "tests.subfile.yaml")
    schema = load_schema_file(schema_filename)
    verify_jsonschema(test_spec, schema)
