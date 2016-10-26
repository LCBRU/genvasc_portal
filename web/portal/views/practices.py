from flask import render_template, request, redirect, url_for, flash
from portal import app, db
from portal.models import *
from portal.forms import *
from portal.helpers import *

@app.route('/practices/')
def practices_index():
    searchForm = SearchForm(formdata = request.args)

    q = PracticeRegistration.query.join(Practice, PracticeRegistration.practice)

    if searchForm.search.data:
        q = q.filter(Practice.name.like("%{0}%".format(searchForm.search.data)))

    registrations = (
        q.order_by(Practice.name.asc())
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False))

    return render_template('practices/index.html', registrations=registrations, searchForm=searchForm)

@app.route('/practices/add/list/')
def practices_add_list():
    searchForm = SearchForm(formdata = request.args)

    q = Practice.query.filter(
        ~Practice.code.in_(db.session.query(PracticeRegistration.code)))

    if searchForm.search.data:
        q = q.filter(Practice.name.like("%{0}%".format(searchForm.search.data)))

    practices = (
        q.order_by(Practice.name.asc())
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False))

    return render_template('practices/add_list.html', practices=practices, searchForm=searchForm)

@app.route('/practices/add/<string:code>', methods=['GET','POST'])
@must_exist(model=Practice, field=Practice.code, request_field='code', error_redirect='practices_add_list', message="Practice does not exist")
def practices_add(code):
    form = PracticeAddForm()

    if form.validate_on_submit():

        pr = PracticeRegistration(
            user=current_user(),
            code=form.code.data,
            date_initiated=form.date_initiated.data,
            notes=form.notes.data
            )

        db.session.add(pr)
        db.session.commit()

        return redirect(url_for('practices_add_list'))

    practice = Practice.query.filter(Practice.code == code).first()
    form = PracticeAddForm(code=code)

    return render_template('practices/edit.html', form=form, practice=practice, cancel_link='practices_add_list')

@app.route('/practices/edit/<string:code>', methods=['GET','POST'])
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def practices_edit(code):
    form = PracticeEditForm()

    pr = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    if form.validate_on_submit():
        pr.date_initiated=form.date_initiated.data
        pr.notes=form.notes.data
        db.session.commit()

        return redirect(url_for('practices_index'))

    practice = Practice.query.filter(Practice.code == code).first()
    form = PracticeEditForm(obj=pr)

    return render_template('practices/edit.html', form=form, practice=practice, cancel_link='practices_index')

@app.route('/practices/delete/<string:code>')
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def practices_delete(code):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()
    form = DeleteForm(obj=practice_registration)
    return render_template('practices/delete.html', form=form, practice_registration=practice_registration)

@app.route('/practices/delete/<string:code>', methods=['POST'])
def practices_delete_confirm(code):
    form = DeleteForm()

    if form.validate_on_submit():
        pr = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()
        practice = Practice.query.filter(Practice.code == code).first()

        if (pr):
            db.session.delete(pr)
            db.session.commit()
            flash("Deleted practice regsitration for {}.".format(practice.name))
            
    return redirect(url_for('practices_index'))

def current_user():
    return User.query.filter(User.username == 'richard').first()
