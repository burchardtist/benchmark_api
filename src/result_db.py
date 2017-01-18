import os

import numpy as np
from decimal import Decimal
from sqlalchemy import create_engine

from src.settings import STATUSES, MYSQL_TABLE, DB_IDS
if os.environ.get('localhost_app'):
    from src.settings import MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_DB


class ResultDB:
    insert_query = 'INSERT INTO {0}({1}) VALUES({2}) RETURNING id;'
    update_status_query = 'UPDATE {0} SET status={1} WHERE id={2};'
    update_results_query = 'UPDATE {0} SET score={1}, {2} WHERE id={3};'
    get_status_query = 'SELECT status from {0} WHERE id={1};'
    get_benchmark_query = 'SELECT * from {0} WHERE id={1};'
    get_all_query = 'SELECT * from {0} where db_system={1} and status=\'done\';'

    def __init__(self):
        self.url = 'postgresql+psycopg2://{user}:{passwd}@{host}/{dbname}'.format(
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            host=MYSQL_HOST,
            dbname=MYSQL_DB
        ) if os.environ.get('localhost_app') else os.environ.get('DATABASE_URL')
        self.conn = create_engine(self.url, isolation_level='AUTOCOMMIT')

    def create_benchmark(self, system, name):
        query = self.insert_query.format(
            MYSQL_TABLE,
            'status, db_system, db_name',
            ''.join('{},'.format(self.escape_values(x)) for x in [STATUSES['IN_PROGRESS'], system, name]).rstrip(',')
        )
        return self.conn.execute(query).fetchone()[0], STATUSES['IN_PROGRESS']

    def update_status(self, benchmark_id, status):
        query = self.update_status_query.format(
            MYSQL_TABLE,
            self.escape_values(status),
            benchmark_id
        )
        self.conn.execute(query)

    def update_results(self, benchmark_id, results):
        query = self.update_results_query.format(
            MYSQL_TABLE,
            sum(results.values()),
            ''.join(['{}_time={},'.format(key, value) for key, value in results.items()]).rstrip(','),
            benchmark_id
        )
        self.conn.execute(query)

    def get_status(self, benchmark_id):
        query = self.get_status_query.format(
            MYSQL_TABLE,
            benchmark_id
        )
        return self.conn.execute(query).fetchone()[0]

    def get_results(self, benchmark_id):
        query = self.get_benchmark_query.format(
            MYSQL_TABLE,
            benchmark_id
        )
        benchmark = dict(zip(self.conn.execute(query).keys(), self.conn.execute(query).fetchone()))
        query_all = self.get_all_query.format(
            MYSQL_TABLE,
            self.escape_values(benchmark['db_system'])
        )
        all_result = self.conn.execute(query_all)
        all_benchmarks = sorted([dict(zip(all_result.keys(), x)) for x in self.conn.execute(query_all)],
                                key=lambda x: x['score'])
        all_benchmarks = [self.replace_decimals(x) for x in all_benchmarks]

        scores = [(float(x['score']), str(x['id'])) for x in all_benchmarks]
        quantiles = [
            all_benchmarks[int(x*len(scores)-1)]
            for name, x in [('first', 0.25), ('second', 0.50), ('third', 0.75)]
        ]

        return dict(
            systemName=next(name.upper() for name, id_ in DB_IDS.items() if str(id_) == benchmark['db_system']),
            totalBenchmarksCount=len(all_benchmarks),
            bestTotalTime=all_benchmarks[0],
            worstTotalTime=all_benchmarks[-1],
            rankingPosition=next(i for i, x in enumerate(all_benchmarks) if str(x['id']) == benchmark_id),
            systemOtherResults=quantiles,
            scoresList=scores
        )

    def escape_values(self, s):
        return '\'{}\''.format(s)

    def replace_decimals(self, item):
        result = {}
        for key, value in item.items():
            result[key] = float(value) if isinstance(value, Decimal) else str(value)
        return result


