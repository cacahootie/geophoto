import os

from flask import Flask

basedir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(basedir,'static','index.html')

app = Flask(
    'geophoto',
    static_folder=os.path.join(basedir,'static'),
    static_url_path='/static'
)

import views
