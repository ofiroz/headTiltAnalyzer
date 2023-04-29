from typing import Union, Any


def add_to_dict(dic: dict, key: Union[int, str], value: Any, default: Any = None):
    dic[key] = dic.get(key, default) + 1