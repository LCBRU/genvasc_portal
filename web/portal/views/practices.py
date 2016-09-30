from flask import render_template, request, redirect, url_for

from portal import app, db

from portal.models import *

@app.route('/practices', methods=['GET'])
def practices_index():
    practices = PracticeRegistration.query.order_by(PracticeRegistration.date_created.desc()).all()
    return render_template('practices/index.html', practices=practices)

@app.route('/practices/add/list', methods=['GET'])
def practices_add_list():
    practices = Practice.query.order_by(Practice.name.asc()).all()
    return render_template('practices/add_list.html', practices=practices)

@app.route('/practices/add/select', methods=['POST'])
def practices_add():
    name = request.form['name']
    code = request.form['code']
    practice = Practice(name, code)
    db.session.add(practice)
    db.session.commit()

    return redirect(url_for('practices_index'))