def partial(value: dict, schema) -> dict:
    return __dict_fetch(value, schema)


def __dict_fetch(_dict: dict, key) -> dict:
    if isinstance(key, list):
        return {_key: _val for k in key for _key, _val in __dict_fetch(_dict, k).items()}

    if isinstance(key, dict):
        return {k: __dict_fetch(_dict.get(k), v) for k, v in key.items()}
        # return {_key: _val for k, v in key.items() for _key, _val in __dict_fetch(_dict.get(k), v).items()}

    else:
        return {key: _dict.get(key)}

# def __dict_fetch_dict(_dict: dict, key, value)-> dict:
#   val


dic = {'a': 3, 'b': {'c': 1, 'd': 2}}
print(partial(dic, ['a', {'b': 'd'}]))
