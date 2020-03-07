from collections import Iterable


def flat(data, parent_dir):
    """
    Converts a dictionary with nested entries like this
        {
            "dict1": {
                "dict2": {
                    "key1": value1,
                    "key2": value2,
                    ...
                },
                ...
            },
            ...
            "dict3": {
                "key3": value3,
                "key4": value4,
                ...
            }
            ...
        }
    
    to a "flattened" dictionary like this that has no nested entries:
        {
            "dict1.dict2.key1": value1,
            "dict1.dict2.key2": value2,
            ...
            "dict3.key3": value3,
            "dict3.key4": value4,
            ...
        }

    :param Iterable data : json data.
    :param tuple parent_dir: json fields. 

    :return dict: {subtest: value}
    """

    def _helper(data, parent_dir, ret):
        if isinstance(data, list):
            for item in data:
                ret.update(_helper(item, parent_dir, ret))
        elif isinstance(data, dict):
            for k, v in data.items():
                current_dir = parent_dir + (k,)
                subtest = ".".join(current_dir)
                if isinstance(v, Iterable):
                    ret.update(_helper(v, current_dir, ret))
                elif v:
                    ret.setdefault(subtest, []).append(v)
        return ret

    return _helper(data, parent_dir, {})


def get_nested_items(nested_obj, nested_keys):
    """
    This function returns the items found from a nested object by a nested key list. 

    :param Iterable nested_obj: nested data object.
    :param list nested_keys: nested keys.

    :return list: the values found by nested keys.
    """
    ret = []

    def _helper(nested_obj, nested_keys):
        if nested_keys:
            if isinstance(nested_obj, list):
                for entry in nested_obj:
                    _helper(entry, nested_keys)
            elif isinstance(nested_obj, dict) and len(nested_keys) == 1:
                ret.append(nested_obj[nested_keys[0]])
            else:
                _helper(nested_obj[nested_keys[0]], nested_keys[1:])

    _helper(nested_obj, nested_keys)

    return ret
