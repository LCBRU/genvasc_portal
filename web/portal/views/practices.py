from flask import render_template, request, redirect, url_for, flash
from portal import app, db
from portal.models import *
from portal.forms import *

@app.route('/practices/')
@app.route('/practices/<int:page>')
def practices_index(page=1):
    searchString = request.args.get('search')
    searchForm = SearchForm(search=searchString)

    q = PracticeRegistration.query.join(Practice, PracticeRegistration.practice)

    if searchString:
        q = q.filter(Practice.name.like("%{0}%".format(searchString)))

    registrations = (
        q.order_by(Practice.name.asc())
         .paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('practices/index.html', registrations=registrations, searchForm=searchForm)

@app.route('/practices/add/list/')
@app.route("/practices/add/list/<int:page>")
def practices_add_list(page=1):
    searchString = request.args.get('search')
    searchForm = SearchForm(search=searchString)
    selectForm = PracticeRegisterForm()

    q = Practice.query.filter(
        ~Practice.code.in_(db.session.query(PracticeRegistration.code)))

    if searchString:
        q = q.filter(Practice.name.like("%{0}%".format(searchString)))

    practices = (
        q.order_by(Practice.name.asc())
         .paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('practices/add_list.html', practices=practices, searchForm=searchForm, selectForm=selectForm)

@app.route('/practices/add/select', methods=['POST'])
def practices_add():
    form = PracticeRegisterForm()

    if form.validate_on_submit():

        practice = Practice.query.get(form.code.data)

        registration = PracticeRegistration(code=practice.code)

        db.session.add(registration)
        db.session.commit()

        flash("Practice '%s' registered." % practice.name)

    return redirect(url_for('practices_add_list'))
