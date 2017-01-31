import re, datetime
from flask import render_template, request, redirect, url_for, flash
from flask_security import login_required, current_user
from portal import app, db
from portal.models import *
from portal.forms import *
from portal.helpers import *
from portal.datatypes import *

@app.route('/practices/<string:code>/recruits')
@app.route('/practices/<string:code>')
@login_required
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def recruits_index(code):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    searchForm = SearchForm(formdata = request.args)

    q = Recruit.query.join(PracticeRegistration, Recruit.practice_registration).filter(PracticeRegistration.code == code)

    if searchForm.search.data:
        # TODO
        q = q.filter(Recruit.nhs_number.like("%{}%".format(searchForm.search.data)))

    recruits = (
        q.order_by(Recruit.date_recruited.desc())
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False))

    return render_template('practices/recruits/index.html', recruits=recruits, practice_registration=practice_registration, searchForm=searchForm)

@app.route('/practices/<string:code>/recruits/add', methods=['GET','POST'])
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
@login_required
def recruits_add(code):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    form = RecruitNewForm()

    if form.validate_on_submit():

        recruit = Recruit(
            practice_registration = practice_registration,
            user = current_user,
            nhs_number = NhsNumberHelper.format(form.nhs_number.data),
            date_of_birth = form.get_date_of_birth(),
            date_recruited = form.date_recruited.data,
            )

        db.session.add(recruit)
        db.session.commit()

        return redirect(url_for('recruits_index', code=code))

    form = RecruitNewForm(code = code)

    return render_template('practices/recruits/edit.html', form=form, practice_registration=practice_registration)

@app.route('/practices/<string:code>/recruits/<string:id>/edit', methods=['GET','POST'])
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
@must_exist(model=Recruit, field=Recruit.id, request_field='id', error_redirect='practices_index', message="Recruit does not exist")
@recruit_is_portal_created()
@login_required
def recruits_edit(code, id):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()
    recruit = Recruit.query.get(id)

    form = RecruitEditForm()

    if form.validate_on_submit():

        recruit.nhs_number = NhsNumberHelper.format(form.nhs_number.data)
        recruit.date_of_birth = form.get_date_of_birth()
        recruit.date_recruited = form.date_recruited.data

        db.session.commit()

        return redirect(url_for('recruits_index', code=code))

    form = RecruitEditForm(obj=recruit)

    return render_template('practices/recruits/edit.html', form=form, practice_registration=practice_registration)