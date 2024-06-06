import re
from typing import MutableMapping


def replace_placeholders(to_replace_dict: MutableMapping, extra_value: MutableMapping) -> MutableMapping:
    """
    replace the placeholder with value in parametrize
    """
    pattern = re.compile(r'{(\w+)}')

    def replacer(v):
        if isinstance(v, str):
            matches = pattern.findall(v)
            for match in matches:
                if match in extra_value:
                    original_value = extra_value[match]
                    v = v.replace(f'{{{match}}}', str(original_value))
                    # 转换回原始类型
                    if isinstance(original_value, int):
                        return int(v)
                    elif isinstance(original_value, float):
                        return float(v)
                    elif isinstance(original_value, bool):
                        return v.lower() in ('true', '1')
        return v

    for key, value in to_replace_dict.items():
        if isinstance(value, dict):
            to_replace_dict[key] = replace_placeholders(value, extra_value)
        elif isinstance(value, list):
            to_replace_dict[key] = [
                replace_placeholders(item, extra_value) if isinstance(item, dict) else replacer(item) for item in
                value]
        else:
            to_replace_dict[key] = replacer(value)
    return to_replace_dict
