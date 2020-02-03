def flat(data, parent_dir):
    def recursive_helper(data, parent_dir, ret):
        if isinstance(data, list):
            for item in data:
                ret.update(recursive_helper(item, parent_dir, ret))
        elif isinstance(data, dict):
            for k, v in data.items():
                current_dir = parent_dir.copy()
                current_dir.append(k)
                subtest = '.'.join(current_dir)
                if (isinstance(v, dict) and v.values()) or isinstance(v, list):
                    ret.update(recursive_helper(v, current_dir, ret))
                elif v:
                    existed_data = ret.get(subtest)
                    if not existed_data:
                        ret.update({subtest: v})
                    elif isinstance(existed_data, list):
                        existed_data.append(v)
                        ret.update({subtest: existed_data})
                    else:
                        existed_data = [existed_data]
                        existed_data.append(v)
                        ret.update({subtest: existed_data})

        return ret

    return recursive_helper(data, parent_dir, {})
