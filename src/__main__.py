import sys

from sqlalchemy.exc import OperationalError

from src.benchmark import Benchmark
from src.result_db import ResultDB
from src.settings import STATUSES


def run():
    kwargs = {key: value for key, value in (x.split('=') for x in sys.argv[1:])}
    benchmark_id = kwargs['benchmark_id']
    del kwargs['benchmark_id']
    result_db = ResultDB()

    try:
        benchmark = Benchmark(**kwargs)
        benchmark.start_benchmark()
    except OperationalError:
        result_db.update_status(benchmark_id, STATUSES['FAIL'])
        return
    result_db.update_status(benchmark_id, STATUSES['DONE'])
