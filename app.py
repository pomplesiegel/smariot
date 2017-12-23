from flask import Flask
from flask import render_template
import requests
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

app.run(use_reloader=True)
