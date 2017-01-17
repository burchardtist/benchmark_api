from time import time

from src.setup_logger import setup_logger


class Timed:
    def __init__(self):
        self.logger = setup_logger('performance')
        self.operation = None

    def time(self, gen, operation, **kwargs):
        self.operation = operation
        try:
            if 'indexed' in kwargs and kwargs['indexed']:
                self.operation = '{}_{}'.format(self.operation, 'indexed')
            else:
                self.operation = self.operation.replace('_indexed', '')

            start = time()
            while True:
                dbsystem, length = next(gen)
        except StopIteration:
            elapsed = time() - start
            self.logger.info("[%s][%s][%s] time: %.3fs" % (length, self.operation, dbsystem, elapsed))
            return elapsed
