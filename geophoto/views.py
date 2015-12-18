
import os

from flask import Flask, jsonify, render_template, request

from geophoto import app, models

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

@app.route("/")
def index():
    return open(index_path).read()

@app.route("/photos/")
def photos():
    return jsonify(models.photos())
