from collections import Iterable


def flat(data, parent_dir):
    '''
    Convert JSON data to a dictionary.

    :param Iterable data : json data.
    :param tuple parent_dir: json fields. 

    :return dict: {subtest:json_value}
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
                    update_value = ret.get(subtest, [])
                    update_value.append(v)
                    ret.update({subtest: update_value})
        return ret

    return _helper(data, parent_dir, {})
