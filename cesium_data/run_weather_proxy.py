from gevent.pywsgi import WSGIServer
from weather_proxy import app

# this one seems alot slower than the development flask server.

http_server = WSGIServer(('127.0.0.1', 80), app)
http_server.serve_forever()