#so that pipreqs adds gunicorn as a dep
import gunicorn
import base64
from flask import Flask, render_template, redirect, url_for, request,jsonify

app = Flask(__name__)

@app.route("/")
def default_route():
    return render_template('index.html')

@app.route("/recv", methods=['POST']) 
def index():
    resp = None
    try:
        req_json = request.get_json(force=True)
        #parse data
        if parse_ttn_message(req_json):
            resp = {'result':'success'}
        else:
            resp = {'result':'failure', 'error':'could not parse request'}
    except:
        resp = {'result':'failure', 'error':'request does not contain JSON'}
    return jsonify(resp)

def parse_ttn_message(msg):
    try:
        recv_data = {}
        recv_data['hardware_serial'] = msg['hardware_serial']
        recv_data['timestamp'] = msg['metadata']['time']
        recv_data['payload_raw'] = base64.b64decode(msg['payload_raw'])
        print(recv_data)
        return True
    except:
        return False

if __name__ == '__main__':
    app.run()
