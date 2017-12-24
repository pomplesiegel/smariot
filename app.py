#so that pipreqs adds gunicorn as a dep
import gunicorn
import base64
from time import gmtime, strftime
from collections import deque
from flask import Flask,render_template,request,jsonify,abort

app = Flask(__name__)

CACHE_SIZE = 5             # max. num requests to keep
RELOAD_INTERVAL = 240      # in seconds

data_cache = deque(maxlen=CACHE_SIZE)

@app.route("/")
def default_handler():
    return render_template('index.html', cache=data_cache, count=CACHE_SIZE,
                                ts=get_timestamp(), refresh=RELOAD_INTERVAL)

@app.route("/data", methods=['GET','POST']) 
def data_handler():
    if request.method == 'POST':
        try:
            add_to_cache(request.get_json(force=True))
            return jsonify({'result':'success'})
        except:
            abort(400)
    elif request.method == 'GET':
       return jsonify(get_cached_data())
    else:
        abort(400)

def get_timestamp():
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

def add_to_cache(data):
    data_cache.append((data, get_timestamp()))

def get_cached_data():
    resp = list()
    for item in data_cache:
        resp.append(item[0])
    return resp

if __name__ == '__main__':
    app.run()
