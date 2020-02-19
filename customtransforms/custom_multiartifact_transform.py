import re
import os

import numpy as np
from sys import stdout
import time

from transformer import Transformer
from logger import NotebookLogger

logger = NotebookLogger()

def write_same_line(msg, sleep_time=0.01):
    stdout.write("\r%s" % str(msg))
    stdout.flush()
    time.sleep(sleep_time)

def finish_same_line():
    stdout.write("\r  \r\n")

class MultiArtifactTransformer(Transformer):
    entry_number = 0

    def merge(self, sde):
        if NotebookLogger.debug:
            finish_same_line()
        merged = {'data': [], 'xaxis': []}

        for entry in sde:
            if type(entry['xaxis']) in (dict, list,):
                raise Exception(
                    "Expecting non-iterable data type in xaxis entry, found %s" % type(entry['xaxis'])
                )

        data = [(entry['xaxis'], entry['data']) for entry in sde]

        dsorted = sorted(data, key=lambda t: t[0])

        for xval, val in dsorted:
            merged['data'].extend(val)
            merged['xaxis'].append(xval)

        self.entry_number = 0
        return merged

    def transform(self, data, path=None):
        self.entry_number += 1

        # Find trial number
        trial_number = self.entry_number
        if path:
            failed = True
            tail = True
            tmppath = path
            while failed and tail:
                head, tail = os.path.split(tmppath)
                tmppath = head
                try:
                    trial_number = int(tail)
                    failed = False
                except:
                    pass

        if NotebookLogger.debug:
            write_same_line("On data point %s" % self.entry_number)
        return [{
            'data': [{path: data}],
            'xaxis': trial_number
        }]

    def process(self, name):
        '''
        Process all the known data into a merged, and standardized data format.

        :param str name: Name of the merged data.
        :return dict: Merged data.
        '''
        trfmdata = []

        for file in self.files:
            data = {}

            # Open data
            try:
                data = self.open_data(file)
            except Exception as e:
                logger.warning("Failed to open file %s, skipping" % file)
                logger.warning("%s %s" % (e.__class__.__name__, e))

            # Transform data
            try:
                data = self.transform(data, path=file)
                if type(data) == list:
                    trfmdata.extend(data)
                else:
                    trfmdata.append(data)
            except Exception as e:
                logger.warning("Failed to transform file %s, skipping" % file)
                logger.warning("%s %s" % (e.__class__.__name__, e))

        merged = self.merge(trfmdata)

        if type(merged) == dict:
            merged['name'] = name
        else:
            for e in merged:
                e['name'] = name

        return merged
