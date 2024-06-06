import pathlib
from typing import MutableMapping, Dict

import allure
import pytest
from box import Box

from pytest_yorick.utils.dict_utils import replace_placeholders
from pytest_yorick.exceptions import YamlException, RequestError, BadSchemaError
from pytest_yorick.httpmessage.http_session import send_request
from pytest_yorick.httpmessage.validate import compare_response
from pytest_yorick.report import wrap_step, wrap_parameter
from pytest_yorick.schema.files import verify_tests
from pytest_yorick.utils.regexp_utils import regexp_search
from pytest_yorick.utils.yaml_func import load_single_yaml


class Runner:
    """
    main class for running test
    """
    file_list: Dict[str, pathlib.Path]
    message_map: Dict[str, Dict[str, Dict]]
    user_data: dict
    step_list: list[tuple]
    path: pathlib.Path
    description: str

    def __init__(self):
        self.file_list = {}
        self.message_map = {}
        self.user_data = {}
        self.step_list = []

    def _load_case(self):
        """
        load all subfile in the case dir
        """
        case_dir = self.path.parent
        for file in case_dir.iterdir():
            if file != self.path:
                self.file_list[file.name] = file
        self.__load_test_spec()

    def __load_test_spec(self):
        """
        load test spec from both main and sub files
        :return:
        """
        self.description = self.spec.get('description')
        self.param_vals = self.__get_param_vals()
        if self.param_vals:
            wrap_parameter(self.param_vals)
            self.spec = replace_placeholders(self.spec, self.param_vals)
        try:
            for k, v in self.spec['file-list'].items():
                if isinstance(v, str):
                    v = v.replace("<Test-Case-Name>", self.path.stem)
                    try:
                        file = self.file_list[v]
                        message_dict = Box(load_single_yaml(file))
                        if self.param_vals:
                            message_dict = replace_placeholders(message_dict, self.param_vals)
                        try:
                            verify_tests(message_dict, False)
                        except Exception:
                            raise BadSchemaError(f" BadSchemaError in {file.name}")
                        self.__load_sub_file_box(k, message_dict)
                    except KeyError as e:
                        raise YamlException(e)
                    continue
                raise ValueError
        except (ValueError, KeyError) as e:
            raise e
        self.user_data = self.spec.get('user-data')
        step_list = self.spec.get('test-steps')
        for step in step_list:
            if isinstance(step, dict):
                step_info = (step.get('node-name'), step.get('message-id'))
                self.step_list.append(step_info)

    def __load_sub_file(self, node: str, data: dict):
        self.message_map[node] = {}
        if "MessageList" in data and data['MessageList'] is not None:
            for k, v in data['MessageList'].items():
                self.message_map[node][k] = v
        elif 'MysqlList' in data and data['MysqlList'] is not None:
            # TBD
            pass

    def __load_sub_file_box(self, node: str, data: Box):
        self.message_map[node] = {}
        if data.MessageList:
            for k, v in data.MessageList.items():
                self.message_map[node][k] = v
        elif data.MysqlList:
            # TBD
            pass

    def _run_steps(self):
        for idx, v in enumerate(self.step_list):
            allure_name = "Step {}: {}".format(idx + 1, v[1])
            step = wrap_step(allure_name, self._run_step)
            step(v)

    def _run_step(self, step: tuple):
        message_info = Box(self.message_map[step[0]][step[1]])
        if message_info.HttpMessage:
            try:
                res = send_request(message_info.HttpMessage.Request)
            except Exception as e:
                raise RequestError(f"{step[1]}: Fail to send Request: {e}") from e
            expected_res = message_info.HttpMessage.Response
            if expected_res:
                try:
                    compare_response(expected_res, res)
                except Exception as e:
                    raise AssertionError(f"{step[1]}: Assertion failed: {e}") from e
        # elif "Mysql" in message_info:
        #     # todo: to support Mysql case

    def _cleanup(self):
        self.file_list.clear()
        self.message_map.clear()
        self.user_data.clear()
        self.spec.clear()
        self.step_list.clear()
        self.description = ""

    def __get_param_vals(self):
        extra_values = self.spec.get('extra-values', [])
        if extra_values:
            for v in extra_values:
                pattern = r"^parametrized\[[^\]]+\]$"
                if isinstance(v, dict) and regexp_search(pattern, v['name']):
                    return v['variables']
        return None

    def __call__(self, path: pathlib.Path, spec: MutableMapping):
        self.path = path
        self.spec = spec
        try:
            self._load_case()
        except Exception as e:
            pytest.fail(f"_load_case raised an exception: {e}")
        try:
            self._run_steps()
        except Exception as e:
            pytest.fail(f"Step: {e}")
        finally:
            self._cleanup()


run_test = Runner()
