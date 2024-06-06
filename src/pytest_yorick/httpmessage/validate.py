from requests import Response
from pytest_yorick import exceptions
from pytest_yorick.report import attach_yaml


def compare_values(expected, actual, path=""):
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in expected:
            if key not in actual:
                raise exceptions.MissingKeyError(key, path)
            compare_values(expected[key], actual[key], path + key + ".")
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            raise exceptions.LengthMismatchError(len(expected), len(actual), path)
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            compare_values(expected_item, actual_item, path + f"[{index}].")
    else:
        if expected != actual:
            raise exceptions.ValueMismatchError(expected, actual, path)


def compare_response(expected_data: dict, response: Response) -> bool:
    # 比较状态码
    status_code = expected_data.get('StatusCode')
    if status_code and response.status_code != status_code:
        raise exceptions.StatusCodeMismatchError(status_code, response.status_code)

    # 比较响应体
    exp_res_body = expected_data.get('ResponseBody')
    act_res_body = response.json()
    attach_yaml(exp_res_body, 'Expected Response info')
    attach_yaml(act_res_body, 'Received Response info')
    compare_values(exp_res_body, act_res_body)
    return True
