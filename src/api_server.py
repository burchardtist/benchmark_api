import bottle
import subprocess
from bottle import request, response

from src.result_db import ResultDB

app = bottle.Bottle()
response.default_content_type = "application/json"

result_db = ResultDB()


@app.post('/RegisterBenchmark')
def listing_handler():
    """
    try:
        params = {key: request.POST[key] for key in ['systemId', 'address', 'port', 'user', 'password']}
    except KeyError:
        return {
            'error': 'too few arguments'
        }
    """
    benchmark_id, status = result_db.create_benchmark()
    proc_string = 'start_benchmark host={} user={} password={} db_name={} db_id={} benchmark_id={}'.format(
        'localhost', 'root', 'admin123', 'comparison', '1', benchmark_id
    )

    subprocess.Popen(proc_string.split())
    return {
        'benchmark_id': benchmark_id,
        'status': status
    }


def run_server():
    bottle.run(app, host='localhost', port=8080)


if __name__ == '__main__':
    run_server()
