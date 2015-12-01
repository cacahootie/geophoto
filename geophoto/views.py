
import os

from flask import Flask, jsonify, render_template, request

from geophoto import app

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

@app.route("/")
def index():
    return open(index_path).read()

@app.route("/photos/")
def photos():
    return jsonify({"results":[
        {
            "src":"/static/img/02.jpg",
            "lat":"37.445711",
            "lng":"-105.594985",
            "id":"02"
        },
        {
            "src":"/static/img/03.jpg",
            "lat":"35.759139",
            "lng":"140.387252",
            "id":"03"
        },
        {
            "src":"/static/img/04.jpg",
            "lat":"1.280231",
            "lng":"103.844888",
            "id":"04"
        }
    ]})
