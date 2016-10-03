from flask import render_template, request

from portal import app, db

from portal.models import *

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
