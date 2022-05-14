from types import SimpleNamespace
class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)

def __dict_fetch(dictionary: dict, key, to_dict=True, raises=False) -> dict:
    if dictionary is None:
        return

    __dict = dictionary

    if not isinstance(__dict, dict):
        if to_dict:
            if hasattr(__dict, 'to_dict'):
                __dict = dictionary.to_dict()
            elif raises:
                raise TypeError(
                    f'Object with key {key} is of type <{type(__dict)}>, and cannot be transformed to <dict>')
            else:
                return
        else:
            return

    if isinstance(key, list):
        return {key_key: key_val for k in key for key_key, key_val in __dict_fetch(__dict, k).items()}

    if isinstance(key, dict):
        return {k: __dict_fetch(__dict.get(k), v) if __dict else None for k, v in key.items()}

    else:
        return {key: __dict.get(key)}


def partial_dict(_dict: dict, schema, to_dict=True, raises=False) -> dict:
    return __dict_fetch(_dict, schema, to_dict, raises)
