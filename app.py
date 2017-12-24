#gunicorn so that pipreqs adds it as a dep in requirements.txt
import gunicorn, base64, os, psycopg2, datetime, json
from urllib import parse
from time import gmtime, strftime
from collections import deque
from flask import Flask,render_template,request,jsonify,abort
from flask_sqlalchemy import SQLAlchemy

CACHE_SIZE = 5                                  # max. num requests to keep
RELOAD_INTERVAL = 240                           # in seconds
data_cache = deque(maxlen=CACHE_SIZE)           # holds latest 5 messages

app = Flask(__name__)

# DB config settings, the second one is to supress a warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ORM Class for the data
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    msg = db.Column(db.String)

    def __init__(self, msg):
        self.msg = msg

@app.route("/")
def default_handler():
    return render_template('index.html', cache=data_cache, count=CACHE_SIZE,
                                ts=get_timestamp(), refresh=RELOAD_INTERVAL)

@app.route("/data", methods=['GET','POST']) 
def data_handler():
    if request.method == 'POST':
        #try:
            add_to_cache(request.get_json(force=True))
            return jsonify({'result':'success'})
        #except:
        #    abort(400)
    elif request.method == 'GET':
       return jsonify(get_cached_data())
    else:
        abort(400)

def get_timestamp():
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

def add_to_cache(data):
    data_cache.append((data, get_timestamp()))
    db_data = Data(json.dumps(data))
    db.session.add(db_data)
    db.session.commit()

def get_cached_data():
    resp = list()
    for item in data_cache:
        resp.append(item[0])
    return resp

if __name__ == '__main__':
    app.run()
