""" smariot : barebones REST App for IoT """
import os
import datetime
import json
import base64
import struct
from time import gmtime, strftime
import dateutil.parser

from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

RELOAD_INTERVAL = 3000                          # in seconds
VIZ_DATA_POINTS = 50                            # default data points for the chart
REC_FETCH_COUNT = '1'                           # default records to fetch (must be a string)

app = Flask(__name__)
socketio = SocketIO(app)

# DB config settings, the second one is to supress a warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Get API Key for env vars (can be set via Heroku Dashboard)
API_KEY = os.environ['API_KEY']


class SensorData(db.Model): # pylint: disable=too-few-public-methods
    """ ORM class for sensor readings """
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    hw_id = db.Column(db.String)
    msg = db.Column(db.String)

    def __init__(self, hw_id, msg):
        self.hw_id = hw_id
        self.msg = msg

    def __str__(self):
        return "SensorData({},{},{})".format(self.timestamp, self.hw_id, self.msg)


class DeviceData(db.Model): # pylint: disable=too-few-public-methods
    """ ORM class for device info """
    __tablename__ = 'device_data'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    hw_id = db.Column(db.String)

    def __init__(self, hw_id):
        self.hw_id = hw_id

    def __str__(self):
        return "DeviceData({},{})".format(self.timestamp, self.hw_id)


@app.route("/")
def default_handler():
    """handler for / endpoint"""
    return render_template('index.html')


@app.route("/req")
def req_handler():
    """handler for request iframe"""
    return render_template('req.html', refresh=RELOAD_INTERVAL)


@app.route("/data", methods=['GET', 'POST'])
def data_handler():
    """handler for /data endpoint"""
    if request.method == 'POST':
        key = request.headers['x-api-key']
        if not key == API_KEY:
            abort(401)
        else:
            try:
                save_and_emit(request.get_json(force=True))
                return jsonify({'result': 'success'})
            except:
                abort(400)
    elif request.method == 'GET':
        return db_fetch_handler()
    else:
        abort(400)


@app.route("/db")
@app.route("/db/<count>")
def db_fetch_handler(count=REC_FETCH_COUNT):
    """ handler for /db endpoint -- fetch data from DB"""
    dat = db.session.query(SensorData).order_by(SensorData.id.desc()).limit(count)
    ret_list = list()
    for item in dat:
        ret_list.append({'hw_id':item.hw_id,
                         'timestamp': item.timestamp,
                         'data':json.loads(item.msg)})
    return jsonify(ret_list)


@app.route("/viz")
@app.route("/viz/<dev_id>")
def viz_handler(dev_id=''):
    """ handler for the viz endpoint """
    if not dev_id:
        return render_template('viz.html', dev_list=get_dev_list())
    else:
        viz = get_viz_data(dev_id)
        return render_template('viz_chart.html', refresh=RELOAD_INTERVAL, viz_data=viz)


@socketio.on('connect', namespace='/live')
def client_connect():
    """ socketio client connect handler """
    emit('my response', {'data': 'Connected'})


def get_timestamp():
    """returns UTC time in readable format"""
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())


def save_and_emit(data):
    """ save POSTed data to DB and emit to socketio """
    readings = msg_get_value(data)
    hwid = msg_get_hw_id(data)

    # parse sensor data and add to DB
    sensor_data = SensorData(hwid, json.dumps(readings))
    db.session.add(sensor_data)

    # parse Hardware ID and add to DB, if not existing
    dev_data = get_or_create(db.session, DeviceData, hw_id=hwid)
    if dev_data:
        db.session.add(dev_data)

    # save changes to DB
    db.session.commit()

    # emit raw JSON to socketio (so that it shows up on homepage)
    socketio.emit('data', {'timestamp': get_timestamp(), 'value': json.dumps(data)},
                  namespace='/live')


def get_viz_data(device_id, count=VIZ_DATA_POINTS):
    """ fetch data from DB and parse for visualization"""
    return parse_db_data(device_id, count)


def parse_db_data(device_id, count):
    """ parses stored JSON and returns plottable data (timestamp vs sensor value) """
    dat = db.session.query(SensorData).filter(SensorData.hw_id.like(device_id)) \
                .order_by(SensorData.id.desc()).limit(count)
    dat_list = list()
    for item in dat:
        timestamp = item.timestamp
        val = json.loads(item.msg)
        dat_list.append((timestamp, val))
    return list(reversed(dat_list))


def msg_get_timestamp(raw_json):
    """ extract timestamp from JSON """
    return dateutil.parser.parse(raw_json['metadata']['time']).strftime("%d/%m/%y %H:%M:%S")


def msg_get_value(raw_json):
    """ extract sensor reading from JSON """
    return msg_parse_val(raw_json['payload_raw'])


def msg_parse_val(raw_val):
    """ parse JSON from TTN and return actual sensor value """
    ret_val = 0
    try:
        # extract sensor values (2x floats)
        byte_arr = base64.b64decode(raw_val)
        ret_val = struct.unpack('ff', byte_arr)
    except:
        pass
    return ret_val


def msg_get_hw_id(raw_json):
    """ extract hardware ID from JSON """
    return raw_json['hardware_serial']


# see https://stackoverflow.com/q/2546207
def get_or_create(session, model, **kwargs):
    """ helper method to insert in DB if not exist """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_dev_list():
    """ get list of hardware IDs in DB"""
    dat = db.session.query(DeviceData).order_by(DeviceData.id.desc())
    dat_list = list()
    for item in dat:
        dat_list.append(str(item.hw_id))
    return list(reversed(dat_list))


if __name__ == '__main__':
    socketio.run(app)
