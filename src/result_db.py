from sqlalchemy import create_engine

from src.settings import MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_DB, MYSQL_TABLE, STATUSES


class ResultDB:
    insert_query = 'INSERT INTO {0}({1}) VALUES({2});'
    update_status_query = 'UPDATE {0} SET status={1} WHERE id={2};'

    def __init__(self):
        self.url = 'mysql+pymysql://{user}:{passwd}@{host}/{dbname}'.format(
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            host=MYSQL_HOST,
            dbname=MYSQL_DB
        )
        self.conn = create_engine(self.url)

    def create_benchmark(self):
        query = self.insert_query.format(
            MYSQL_TABLE,
            'status',
            self.escape_values(STATUSES['IN_PROGRESS'])
        )
        result = self.conn.execute(query)
        import ipdb
        ipdb.set_trace()
        return result.lastrowid, STATUSES['IN_PROGRESS']

    def update_status(self, benchmark_id, status):
        query = self.update_status_query.format(
            MYSQL_TABLE,
            self.escape_values(status),
            benchmark_id
        )
        self.conn.execute(query)

    def escape_values(self, s):
        return '\'{}\''.format(s)
