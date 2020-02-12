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

        for k, v in flat(data, ()).items():
            ret.append({
                'data': [{'value': i, 'xaxis': self.entry_number} for i in v],
                'subtest': k
            })

        return ret

    def merge(self, data):
        return data
