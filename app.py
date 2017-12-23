#so that pipreqs adds gunicorn as a dep
import gunicorn
import base64
from time import gmtime, strftime
from collections import deque
from flask import Flask,render_template,request,jsonify,abort

app = Flask(__name__)

MAX_REQ_TO_KEEP = 5             # max. num requests to keep
PAGE_RELOAD_INTERVAL = 240      # in seconds

last_recv_data = deque(maxlen=MAX_REQ_TO_KEEP)

def get_timestamp():
    return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

@app.route("/")
def default_route():
    return render_template('index.html', result=last_recv_data, count=MAX_REQ_TO_KEEP,
                                ts=get_timestamp(), refresh=PAGE_RELOAD_INTERVAL)

@app.route("/data", methods=['GET','POST']) 
def index():
    resp = None
    if request.method == 'POST':
        try:
            global last_recv_data
            last_recv_data.append((request.get_json(force=True), get_timestamp()))
            resp = {'result':'success'}
            return jsonify(resp)
        except:
            abort(400)
    else:
        resp = list()
        for item in last_recv_data:
            resp.append(item)
        return jsonify(resp)

if __name__ == '__main__':
    app.run(debug=True)
