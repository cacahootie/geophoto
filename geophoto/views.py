
import os
from functools import wraps

from flask import Flask, jsonify, render_template, request, abort

from geophoto import app, models, oembed

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

def spa(vfunc):
	@wraps(vfunc)
	def wrapper(*args, **kwargs):
		if request.args.get('format') == 'json':
			return vfunc(*args, **kwargs)
		else:
			return render_template('index.html')
	return wrapper

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/photos/")
@spa
def photos():
    return jsonify(models.photos())

@app.route("/articles/")
@spa
def articles():
    return jsonify(models.articles())

@app.route("/articles/<key>/")
@spa
def article(key):
	return jsonify(models.article(key))

@app.route("/tags/<id>/", methods=["GET",]) 
@spa
def tags(id):
    return jsonify(models.tags(id))

@app.route("/services/oembed/", methods=["GET",]) 
def oembed_service():
    fmt = request.args.get("format")
    if fmt is None or fmt == 'json':
        return jsonify(oembed.oembed(request.args.get('url')))
    elif fmt == 'html':
        return oembed.oembed(request.args.get('url'))
    abort(500)

@app.route("/tags/<id>/", methods=["POST",]) 
@spa
def add_tags(id):
    try:
        return jsonify(models.add_tags(id, request.get_json()))
    except ValueError:
        abort(409)
