import bottle
from bottle import request, response
from bottle import post, get


app = bottle.Bottle()


@app.get('/names')
def listing_handler():
    import ipdb
    ipdb.set_trace()
    pass

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080)
