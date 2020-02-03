def flat(data: dict, subtest: str):
    ret = {}

    for k, v in data.items():
        subtest_children = '.'.join((subtest, k))
        if isinstance(v, dict) and v.values():
            ret.update(flat(v, subtest_children))
        elif v or v == 0:
            ret.update({subtest_children: v})

    return ret
