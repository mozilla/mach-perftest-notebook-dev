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
            ret.append({
                'data': bs['pageinfo']['navigationStartTime'],
                'xaxis': self.entry_number,
                'subtest': 'browserScripts.pageinfo.navigationStartTime'
            })

            flatted_timings = flat(bs['timings'], 'browserScripts.timings')

            for k, v in flatted_timings.items():
                ret.append({
                    'data': v,
                    'xaxis': self.entry_number,
                    'subtest': k
                })

        return ret

    def merge(self, data):
        # return data
        grouped_data = {}
        for entry in data:
            # print(entry)
            subtest = entry['subtest']
            if subtest not in grouped_data:
                grouped_data[subtest] = []
            grouped_data[subtest].append(entry)

        merged_data = []
        for subtest in grouped_data:
            data = [(entry['xaxis'], entry['data'])
                    for entry in grouped_data[subtest]]

            dsorted = sorted(data, key=lambda t: t[0])

            merged = {'data': [], 'xaxis': []}
            for xval, val in dsorted:
                merged['data'].append(val)
                merged['xaxis'].append(xval)
            merged['subtest'] = subtest

            merged_data.append(merged)

        self.entry_number = 0
        return merged_data
