MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'postgres'
MYSQL_PASSWD = 'admin123'
MYSQL_DB = 'benchmark_api'

MYSQL_TABLE = 'benchmark'

STATUSES = dict(
    IN_PROGRESS='in_progress',
    FAIL='fail',
    DONE='done'
)

TABLE_NAME = 'testtable'
TABLE_SIZE = pow(10, 1)

BENCHMARK_ITERATIONS = 2

DB_IDS = dict(
    MYSQL=1,
    POSTGRESQL=2
)

CONNECTORS = dict(
    MYSQL='mysql+pymysql',
    POSTGRESQL='postgresql+psycopg2'
)

TABLE_COLUMNS = {
    'MYSQL': {
        'id': 'int PRIMARY KEY NOT NULL AUTO_INCREMENT',
        'city': 'varchar(255)',
        'lat': 'float(13,10)',
        'lon': 'float(13,10)',
        'date': 'datetime'
    },
    'POSTGRESQL': {
        'id': 'serial PRIMARY KEY NOT NULL',
        'city': 'varchar(255)',
        'lat': 'decimal(13,10)',
        'lon': 'decimal(13,10)',
        'date': 'timestamp'
    }
}

QUERIES = {
    'MYSQL': {
        'create_table': 'DROP TABLE IF EXISTS {0}; CREATE TABLE {0}({1});',
        'insert': 'INSERT INTO {0}({1}) VALUES({2});',
        'select': 'SELECT * FROM {0} where {1};',
        'update': 'UPDATE {0} SET {1} WHERE {2};',
        'create_index': 'ALTER TABLE {0} ADD INDEX({1});',
    },
    'POSTGRESQL': {
        'create_table': 'DROP TABLE IF EXISTS {0}; CREATE TABLE {0}({1});',
        'insert': 'INSERT INTO {0}({1}) VALUES({2});',
        'select': 'SELECT * FROM {0} where {1};',
        'update': 'UPDATE {0} SET {1} WHERE {2};',
        'create_index': 'CREATE INDEX {2} ON {0}({1});',
    }
}
