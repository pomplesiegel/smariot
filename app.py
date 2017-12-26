""" smariot : barebones REST App for IoT """
import os
import datetime
import json
import base64
from time import gmtime, strftime
from collections import deque
import dateutil.parser

# unused, yet imported so pipreqs generates correct requirements.txt
import gunicorn
import psycopg2

from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy


CACHE_SIZE = 5                                  # max. num requests to keep
RELOAD_INTERVAL = 240                           # in seconds
data_cache = deque(maxlen=CACHE_SIZE)           # holds latest 5 messages
VIZ_DATA_POINTS = 50                            # default data points for the chart


app = Flask(__name__)

# DB config settings, the second one is to supress a warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Get API Key for env vars (can be set via Heroku Dashboard)
API_KEY = os.environ['API_KEY']

class Data(db.Model): # pylint: disable=too-few-public-methods
    """ ORM class for storing messages to DB """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    msg = db.Column(db.String)

    def __init__(self, msg):
        self.msg = msg


@app.route("/")
def default_handler():
    """handler for / endpoint"""
    return render_template('index.html', cache=deque(reversed(data_cache)),
                           count=CACHE_SIZE, ts=get_timestamp(),
                           refresh=RELOAD_INTERVAL)


@app.route("/data", methods=['GET', 'POST'])
def data_handler():
    """handler for /data endpoint"""
    if request.method == 'POST':
        key = request.headers['x-api-key']
        if not key == API_KEY:
            abort(401)
        else:
            try:
                add_to_cache(request.get_json(force=True))
                return jsonify({'result': 'success'})
            except:
                abort(400)
    elif request.method == 'GET':
        return jsonify(get_cached_data())
    else:
        abort(400)


@app.route("/db")
@app.route("/db/<count>")
def db_fetch_handler(count='1'):
    """ handler for /db endpoint -- fetch data from DB"""
    dat = db.session.query(Data).order_by(Data.id.desc()).limit(count)
    ret_list = list()
    for item in dat:
        ret_list.append(json.loads(item.msg))
    return jsonify(ret_list)


@app.route("/viz")
def viz_handler():
    viz = get_viz_data(100)
    return render_template('viz.html', viz_data=viz['data'],
                           min_val=viz['minval'], max_val=viz['maxval'])


def get_timestamp():
    """returns UTC time in readable format"""
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())


def add_to_cache(data):
    """helper for adding POSTed data to cache and persisting to DB"""
    data_cache.append((data, get_timestamp()))
    db_data = Data(json.dumps(data))
    db.session.add(db_data)
    db.session.commit()


def get_cached_data():
    """helper to return data in cache as a list"""
    resp = list()
    for item in data_cache:
        resp.append(item[0])
    return resp


def get_viz_data(count=50):
    """ fetch data from DB and parse for visualization"""
    return parse_msg(count)


def parse_msg(count):
    """ parses stored JSON and returns plottable data (timestamp vs sensor value) """
    dat = db.session.query(Data).order_by(Data.id.desc()).limit(count)
    dat_list = list()
    min_val = 0
    max_val = 0
    for item in dat:
        raw_json = json.loads(item.msg)
        try:
            timestamp = dateutil.parser.parse(raw_json['metadata']['time']).strftime("%d/%m/%y %H:%m:%S")
        except:
            continue
        try:
            val = parse_val(raw_json['payload_raw'])
            if val < min_val:
                min_val = val
            if val > max_val:
                max_val = val
        except:
            val = 0         # error case, unparsable data
        dat_list.append((timestamp, val))
    step_size = max_val / len(dat_list)
    return {'data' : list(reversed(dat_list)), 'minval' : min_val - step_size/2,
            'maxval' : max_val + 2 * step_size}


def parse_val(raw_val):
    """ parse JSON from TTN and return actual sensor value """
    ret_val = 5
    try:
        # extract last byte from message, this is the sensor value
        decoded_byte_arr = base64.b64decode(raw_val)
        ret_val = int(hex(decoded_byte_arr[4]), 16)
    except:
        pass
    return ret_val


if __name__ == '__main__':
    app.run(debug=True)
