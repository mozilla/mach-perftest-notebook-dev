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

        flatted_data = flat(data, [])

        for k, v in flatted_data.items():
            data_obj = []
            for i in v:
                data_obj.append({'value': i, 'xaxis': self.entry_number})
            ret.append({
                'data': data_obj,
                'subtest': k
            })

        return ret

    def merge(self, data):
        return data