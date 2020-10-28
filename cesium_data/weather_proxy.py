
import re
from urllib.parse import urlparse, urlunparse
from flask import Flask, render_template, request, abort, Response, redirect
import requests
import logging

from flask_cors import CORS

app = Flask(__name__.split('.')[0])
CORS(app)

logging.basicConfig(level=logging.INFO)
CHUNK_SIZE = 1024
LOG = logging.getLogger("app.py")

# this will need to be changed
address = ('127.0.0.1', 80)

@app.route('/radar/<path:url>', methods=["GET", "POST"])
def root(url):
    if int(address[1] ) != 80:
        _url = request.url.split(f"{address[0]}:{address[1]}")
    else:
        _url = request.url.split(address[0])
    if 'favicon' not in request.url:
        keys = _url[1].split("/")
        z = int(keys[2])
        x = int(keys[3])
        y = int(keys[4].split(".")[0])
        ext = ".png"
        
        # get timestamps
        r = requests.get("https://api.rainviewer.com/public/maps.json")
        timestamps = r.json()
        #print(timestamps)
        timestamp = timestamps[-1] # get the latest one

        # https://tilecache.rainviewer.com/v2/radar/1603861200/512/2/2/1/1/1_1.png
        
        r = requests.get(f"https://tilecache.rainviewer.com/v2/radar/{timestamp}/512/{z}/{x}/{y}/1/1_1.png")
        #print(r.content)
        return Response(r.content, mimetype="image/png")

    return Response("Nothing sent")

if __name__ == "__main__":
    app.run(address[0], address[1])