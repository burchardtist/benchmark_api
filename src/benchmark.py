import random
import string
from datetime import timedelta, datetime

from sqlalchemy import create_engine
from sqlalchemy import text
from src.result_db import ResultDB

from src.settings import TABLE_COLUMNS, TABLE_NAME, QUERIES, CONNECTORS, BENCHMARK_ITERATIONS, TABLE_SIZE, DB_IDS
from src.setup_logger import setup_logger
from src.timed import Timed

logger = setup_logger('performance')


def print_range(length):
    for i in range(length):
        print('GENERATING: {0} / {1}'.format(i + 1, length), end='\r')
        yield


class DatabaseGenerator:
    data = None
    length = None

    def __init__(self, host, port, user, password, db_name, db_id, length):
        self.length = length
        self.dbsystem = next(name.upper() for name, id_ in DB_IDS.items() if str(id_) == db_id)

        self.QUERIES = QUERIES[self.dbsystem]
        self.TABLE_COLUMNS = TABLE_COLUMNS[self.dbsystem]
        self.config = dict(
            HOST=host,
            USER=user,
            PORT=port,
            PASSWORD=password,
            DB_NAME=db_name,
            CONN=CONNECTORS[self.dbsystem]
        )

        self.conn = self.get_engine()

    def get_engine(self, with_db=True):
        url = '{db}://{user}:{passwd}@{host}:{port}{dbname}'.format(
            db=self.config['CONN'],
            user=self.config['USER'],
            passwd=self.config['PASSWORD'],
            host=self.config['HOST'],
            port=self.config['PORT'],
            dbname='/{}'.format(self.config['DB_NAME']) if with_db else ''
        )
        return create_engine(url, isolation_level='AUTOCOMMIT' if not with_db else 'READ_COMMITTED')

    def recreate_db(self):
        columns = ''.join(['{} {},'.format(x, z) for x, z in self.TABLE_COLUMNS.items()])[:-1]
        self.conn.execute(self.QUERIES['create_table'].format(TABLE_NAME, columns))

    def close(self):
        self.conn.dispose()

    def generate_data(self):
        print('generating data')
        self.data = [
            dict(
                city=self._gen_city(),
                lat=self._gen_lat(),
                lon=self._gen_lon(),
                date=self._gen_date())
            for _ in print_range(self.length)
        ]
        logger.info('LENGTH: {}'.format(self.length))

    def insert_data(self, **kwargs):
        for i, name in self._insert_data(self.data):
            print('[INSERT][{2}]: {0} / {1}'.format(i + 1, self.length, name), end='\r')
        print('')
        yield self.dbsystem, self.length

    def select_data(self, where, **kwargs):
        self.conn.execute(text(self.QUERIES['select'].format(
            TABLE_NAME,
            where
        )))
        yield self.dbsystem, self.length

    def update_data(self, set_, where, **kwargs):
        for i, name in self._update_data(set_, where):
            print('[UPDATE][{2}]: {0} / {1}'.format(i + 1, self.length, name), end='\r')
        print('')
        yield self.dbsystem, self.length

    def add_index(self):
        self.conn.execute(self.QUERIES['create_index'].format(
            TABLE_NAME,
            'city',
            'city_index'
        ))
        self.conn.execute(self.QUERIES['create_index'].format(
            TABLE_NAME,
            'lat',
            'lat_index'
        ))
        print('[ADD_INDEX][{}] done'.format(self.dbsystem))

    def _insert_data(self, data):
        for i, item in enumerate(data):
            self.conn.execute(self.QUERIES['insert'].format(
                TABLE_NAME,
                ','.join([x for x in item]),
                ','.join([self.escape_values(col, val) for col, val in item.items()])
            ))
            yield i, self.dbsystem

    def _update_data(self, set_, where):
        for i in range(self.length):
            self.conn.execute(text(self.QUERIES['update'].format(
                TABLE_NAME,
                set_,
                where
            )))
            yield i, self.dbsystem

    def _gen_city(self):
        length = random.randint(3, 50)
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def _gen_lat(self):
        return round(random.uniform(-90.0, 90.0), 10)

    def _gen_lon(self):
        return round(random.uniform(-180.0, 180.0), 10)

    def _gen_date(self):
        d1 = datetime.strptime('1/1/2000 12:00 AM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('1/1/2010 12:00 AM', '%m/%d/%Y %I:%M %p')

        delta = d2 - d1
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return d1 + timedelta(seconds=random_second)

    def escape_values(self, col, val):
        if col in ['lat', 'lon']:
            return str(val)
        else:
            return '\'{}\''.format(val)


class Benchmark:
    def __init__(self, host, port, user, password, db_name, db_id, benchmark_id):
        self.benchmark_id = benchmark_id
        self.result_db = ResultDB()
        self.timed = Timed()
        self.database_generator = DatabaseGenerator(host, port, user, password, db_name, db_id, TABLE_SIZE)
        self.benchmark_times = dict(
            insert=0,
            select=0,
            update=0,
            select_index=0,
            update_index=0
        )

    def start_benchmark(self):
        self.database_generator.generate_data()
        self._run()
        self.result_db.update_results(self.benchmark_id, self.benchmark_times)

    def _run(self):
        for _ in range(BENCHMARK_ITERATIONS):
            self.database_generator.recreate_db()
            self.benchmark_times['insert'] += self.timed.time(self.database_generator.insert_data(), 'insert')
            self.benchmark_times['select'] += \
                self.timed.time(self.database_generator.select_data('city like \'%ab%\' and lat > 30'), 'select')
            self.benchmark_times['update'] += self.timed.time(self.database_generator.update_data(
                'city=\'1posen\', lat=52.4064, lon=16.9252', 'city like \'%ab%\''), 'update')
            self.database_generator.close()

            self.database_generator.recreate_db()
            self.database_generator.add_index()
            self.benchmark_times['select_index'] +=\
                self.timed.time(
                    self.database_generator.select_data('city like \'%1pos%\' and lat > 30', indexed=True), 'update')
            self.benchmark_times['update_index'] +=\
                self.timed.time(self.database_generator.update_data(
                    'city=\'stadt\', lat=5.40624, lon=1.3252', 'city like \'%1pos%\'', indexed=True), 'update')
            self.database_generator.close()
