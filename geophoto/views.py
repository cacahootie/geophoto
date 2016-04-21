
import os

from flask import Flask, jsonify, render_template, request, abort

from geophoto import app, models

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/photos/")
def photos():
    return jsonify(models.photos())

@app.route("/articles/")
def articles():
    return jsonify(models.articles())

@app.route("/articles/<key>/")
def article(key):
	return jsonify(models.article(key))

@app.route("/tags/<id>/", methods=["GET",]) 
def tags(id):
    return jsonify(models.tags(id))

@app.route("/tags/<id>/", methods=["POST",]) 
def add_tags(id):
    try:
        return jsonify(models.add_tags(id, request.get_json()))
    except ValueError:
        abort(409)
