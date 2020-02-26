from collections import Iterable


def flat(data, parent_dir):
    '''
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
    '''
    def _helper(data, parent_dir, ret):
        if isinstance(data, list):
            for item in data:
                ret.update(_helper(item, parent_dir, ret))
        elif isinstance(data, dict):
            for k, v in data.items():
                current_dir = parent_dir + (k,)
                subtest = '.'.join(current_dir)
                if isinstance(v, Iterable):
                    ret.update(_helper(v, current_dir, ret))
                elif v:
                    ret.setdefault(subtest, []).append(v)
        return ret

    return _helper(data, parent_dir, {})
