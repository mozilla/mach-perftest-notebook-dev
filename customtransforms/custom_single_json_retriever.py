from transformer import Transformer
from utilities import flat


class SingleJsonRetriever(Transformer):
    '''
    Transforms perfherder data into the standardized data format.
    '''
    entry_number = 0

    def transform(self, data):
        ret = []
        self.entry_number += 1

        # flat(data, ()) returns a dict that have one key per dictionary path
        # in the original data.
        for k, v in flat(data, ()).items():
            ret.append({
                'data': [{'value': i, 'xaxis': self.entry_number} for i in v],
                'subtest': k
            })

        return ret

    def merge(self, sde):
        grouped_data = {}
        for entry in sde:
            subtest = entry['subtest']
            data = grouped_data.get(subtest, [])
            data.extend(entry['data'])
            grouped_data.update({subtest: data})

        merged_data = []
        for k, v in grouped_data.items():
            merged_data.append({
                'data': v,
                'subtest': k
            })

        self.entry_number = 0
        return merged_data
