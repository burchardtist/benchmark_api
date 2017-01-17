import os

from sqlalchemy import create_engine

from src.settings import STATUSES
if os.environ.get('localhost_app'):
    from src.settings import MYSQL_PASSWD, MYSQL_HOST, MYSQL_DB, MYSQL_TABLE


class ResultDB:
    insert_query = 'INSERT INTO {0}({1}) VALUES({2});'
    update_status_query = 'UPDATE {0} SET status={1} WHERE id={2};'

    def __init__(self):
        self.url = 'mysql+pymysql://{user}:{passwd}@{host}/{dbname}'.format(
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            host=MYSQL_HOST,
            dbname=MYSQL_DB
        ) if os.environ.get('localhost_app') else os.environ.get('DATABASE_URL')
        self.conn = create_engine(self.url)

    def create_benchmark(self, system, name):
        query = self.insert_query.format(
            MYSQL_TABLE,
            'status, db_system, db_name',
            ''.join('{},'.format(self.escape_values(x)) for x in [STATUSES['IN_PROGRESS'], system, name]).rstrip(',')
        )
        return self.conn.execute(query).lastrowid, STATUSES['IN_PROGRESS']

    def update_status(self, benchmark_id, status):
        query = self.update_status_query.format(
            MYSQL_TABLE,
            self.escape_values(status),
            benchmark_id
        )
        self.conn.execute(query)

    def escape_values(self, s):
        return '\'{}\''.format(s)
