#so that pipreqs adds gunicorn as a dep
import gunicorn
import base64
from collections import deque
from flask import Flask,render_template,request,jsonify,abort

app = Flask(__name__)

MAX_REQ_TO_KEEP = 5
last_recv_data = deque(maxlen=MAX_REQ_TO_KEEP)

@app.route("/")
def default_route():
    return render_template('index.html', result=last_recv_data, count=MAX_REQ_TO_KEEP)

@app.route("/recv", methods=['POST']) 
def index():
    resp = None
    try:
        global last_recv_data
        last_recv_data.append(request.get_json(force=True))
        resp = {'result':'success'}
        return jsonify(resp)
    except:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
