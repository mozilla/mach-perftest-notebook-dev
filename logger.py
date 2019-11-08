import logging

logging.basicConfig(level=logging.INFO)
logger = None


class NotebookLogger(object):
    '''
    Simple logger for perftest-notebook.
    '''

    def __init__(self, name='perftest-notebook'):
        self._logger = logger
        if not self._logger:
            self._logger = logging.getLogger(name)

    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)

    def critical(self, msg):
        self._logger.critical(msg)
