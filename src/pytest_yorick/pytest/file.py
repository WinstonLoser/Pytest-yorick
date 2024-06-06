import copy
import itertools
from typing import Dict, Iterator, List, Mapping, Union, Iterable, Tuple, Any
import pytest
from pytest import Mark
from pytest_yorick.exceptions import BadSchemaError, YamlItemError, YamlFileError
from .item import YamlItem
from pytest_yorick.utils.yaml_func import load_single_yaml
from ..schema.files import verify_tests


class YamlFile(pytest.File):
    """
    YamlFile class for collecting tests from a yaml file.
    """

    def collect(self) -> Iterator[YamlItem]:
        """
        collect func will firstly load main case yaml file
        and generate YamlItem from data
        :return:
        """
        main_data = load_single_yaml(self.path)
        if not main_data:
            raise YamlFileError(f"{self.path.name} is empty")
        try:
            try:
                verify_tests(main_data, True)
            except Exception as e:
                raise BadSchemaError(f"BadSchemaError in {self.path.name}: {e}") from e
            for i in self._generate_items(main_data):
                yield i
        except Exception as e:
            raise YamlItemError(f"Fail to generate YamlItem: {e}") from e

    def _generate_items(self, test_spec: Dict) -> Iterator[YamlItem]:
        """
        _generate_items will generate single or multiple YamlItems
        depends on parametrize mark
        :param test_spec:
        :return:
        """
        item = YamlItem.yamlitem_from_parent(
            test_spec["test-name"], self, test_spec, self.path
        )

        pytest_marks: List[Mark] = []
        parametrize_marks: List[Mapping] = []
        marks = test_spec.get('marks', [])
        if marks:
            for m in marks:
                if isinstance(m, dict):
                    # only keep parametrize for now
                    for k, v in m.items():
                        if k == 'parametrize':
                            pytest_marks.append(getattr(pytest.mark, k)(v))
                            parametrize_marks.append({k: v})
                        # else:
                        #     todo: handle other special marks
                        #     pass
                else:
                    # add normal str marks
                    pytest_marks.append(getattr(pytest.mark, m))

            if parametrize_marks:
                yield from _generate_parametrized_items(
                    self, test_spec, parametrize_marks, pytest_marks
                )
                return
            else:
                item.add_markers(pytest_marks)
        yield item


def _generate_parametrized_items(
        parent: pytest.File,
        test_spec: Dict,
        parametrize_marks: Union[List[Dict] | List[Mapping]],
        pytest_marks: List[pytest.Mark],
) -> Iterator[YamlItem]:
    """
    _generate_parametrized_items modify and generate yamlitem from
    each pair of param

    """
    vals = [i["parametrize"]["vals"] for i in parametrize_marks]

    try:
        combined = itertools.product(*vals)
    except TypeError as e:
        raise BadSchemaError(
            "Invalid match between numbers of keys and number of values in parametrize mark"
        ) from e

    keys: List[str] = [i["parametrize"]["key"] for i in parametrize_marks]
    for combined_values in combined:
        if len(combined_values) != len(keys):
            raise BadSchemaError(
                "Invalid match between numbers of keys and number of values in parametrize mark"
            )
        variables, formatted_str = _generate_parametrized_test_items(
            keys, combined_values
        )
        new_spec = copy.deepcopy(test_spec)
        new_spec["test-name"] = test_spec["test-name"] + f"[{formatted_str}]"
        new_spec.setdefault("extra-values", []).append(
            {
                "name": f"parametrized[{formatted_str}]",
                "variables": variables,
            }
        )
        new_item = YamlItem.yamlitem_from_parent(
            new_spec["test-name"], parent, new_spec, parent.path
        )
        new_item.add_markers(pytest_marks)

        yield new_item


def _generate_parametrized_test_items(
        keys: Iterable[Union[str, List, Tuple]], combined_values: Iterable[Tuple[str, str]]
) -> Tuple[Mapping[str, Any], str]:
    """
    _generate_parametrized_test_items repack all key-value of parametrize list
    """
    flattened_values: List[Iterable[str]] = []
    variables: Dict[str, Any] = {}

    for pair in zip(keys, combined_values):
        key, value = pair
        # key: xxx
        if isinstance(key, str):
            variables[key] = value
            flattened_values.append(value)
        # key: [xxx,yyy]
        else:
            if not isinstance(value, (list, tuple)):
                value = [value]
            if len(value) != len(key):
                raise BadSchemaError(
                    f"Invalid match between numbers of keys and number of values in parametrize mark ({len(key)} keys, {len(value)} values)"
                )
            for subkey, subvalue in zip(key, value):
                variables[subkey] = subvalue
                flattened_values.append(subvalue)
    str_fmt = "-".join(["{}"] * len(flattened_values))
    formatted_str = str_fmt.format(*flattened_values)

    return variables, formatted_str
