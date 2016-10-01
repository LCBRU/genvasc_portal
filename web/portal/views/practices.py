from flask import render_template, request, redirect, url_for
from portal import app, db
from portal.models import *
from portal.forms import *

@app.route('/practices', methods=['GET'])
def practices_index():
    practices = PracticeRegistration.query.order_by(PracticeRegistration.date_created.desc()).all()
    return render_template('practices/index.html', practices=practices)

@app.route('/practices/add/list/')
@app.route("/practices/add/list/<int:page>")
def practices_add_list(page=1):
    searchString = request.args.get('search')
    form = SearchForm(search=searchString)

    q = Practice.query

    if searchString:
        q = q.filter(Practice.name.like("%{0}%".format(searchString)))

    practices = (
        q.order_by(Practice.name.asc())
         .paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('practices/add_list.html', practices=practices, form=form)

@app.route('/practices/add/select', methods=['POST'])
def practices_add():
    name = request.form['name']
    code = request.form['code']
    practice = Practice(name, code)
    db.session.add(practice)
    db.session.commit()

    return redirect(url_for('practices_index'))