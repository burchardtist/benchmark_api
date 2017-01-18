import os

import bottle
import subprocess
from bottle import request, response

from src.result_db import ResultDB

app = bottle.Bottle()
result_db = ResultDB()


@app.route('/static/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root='static/')


@app.get('/')
def index_view():
    return bottle.static_file('index.html', root='static/')


@app.get('/api/GetTest')
def get_test():
    try:
        benchmark_id = request.GET['benchmarkId']
    except KeyError:
        return {
            'error': 'benchmarkId is needed'
        }
    return {
        'benchmark_id': benchmark_id,
        'status': result_db.get_status(benchmark_id)
    }


@app.get('/api/GetList')
def get_list():
    try:
        system_id = request.GET['systemId']
    except KeyError:
        return {
            'error': 'systemId is needed'
        }
    return {'result': result_db.get_list(system_id)}


@app.get('/api/BenchmarkResult')
def benchmark_result():
    try:
        benchmark_id = request.GET['benchmarkId']
    except KeyError:
        return {
            'error': 'benchmarkId needed'
        }
    return result_db.get_results(benchmark_id)


@app.post('/api/RegisterBenchmark')
def register_benchmark():
    try:
        params = {key: request.POST[key] for key in ['systemId', 'address', 'port', 'user', 'password', 'database']}
    except KeyError:
        return {
            'error': 'too few arguments'
        }

    benchmark_id, status = result_db.create_benchmark(params['systemId'], params['database'])
    proc_string = 'start_benchmark host={} port={} user={} password={} db_name={} db_id={} benchmark_id={}'.format(
        params['address'], params['port'], params['user'],
        params['password'], params['database'], params['systemId'], benchmark_id
    )

    subprocess.Popen(proc_string.split())
    return {
        'benchmark_id': benchmark_id,
        'status': status
    }


def run_server():
    bottle.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


if __name__ == '__main__':
    run_server()
