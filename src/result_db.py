import os

from sqlalchemy import create_engine

from src.settings import STATUSES, MYSQL_TABLE
if os.environ.get('localhost_app'):
    from src.settings import MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_DB


class ResultDB:
    insert_query = 'INSERT INTO {0}({1}) VALUES({2}) RETURNING id;'
    update_status_query = 'UPDATE {0} SET status={1} WHERE id={2};'
    update_results_query = 'UPDATE {0} SET score={1}, {2} WHERE id={3};'

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

    def escape_values(self, s):
        return '\'{}\''.format(s)
