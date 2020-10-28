from gevent.pywsgi import WSGIServer
from weather_proxy import app

http_server = WSGIServer(('iorama.geosynergy.com.au', 3000), app)
http_server.serve_forever()