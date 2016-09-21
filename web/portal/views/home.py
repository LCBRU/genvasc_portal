from flask import render_template, request

from portal import app, db

from portal.models import *

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        practice = Practice(name, code)
        db.session.add(practice)
        db.session.commit()
    practices = Practice.query.order_by(Practice.date_created.desc()).all()
    return render_template('index.html', practices=practices)
