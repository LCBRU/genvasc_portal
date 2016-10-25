from flask import render_template, request, redirect, url_for, flash
from portal import app, db
from portal.models import *
from portal.forms import *

@app.route('/practices/<string:code>/recruits')
def recruits_index(code):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    searchForm = SearchForm(formdata = request.args)

    q = Recruit.query.join(PracticeRegistration, Recruit.practice_registration).filter(PracticeRegistration.code == code)

    if searchForm.search.data:
        q = q.filter(Recruit.nhs_number.like("%{}%".format(searchForm.search.data)))

    recruits = (
        q.order_by(Recruit.date_created.desc())
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False))

    return render_template('practices/recruits/index.html', recruits=recruits, practice_registration=practice_registration, searchForm=searchForm)

@app.route('/practices/<string:code>/recruits/add', methods=['GET','POST'])
def recruits_add(code):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    form = RecruitNewForm()

    if form.validate_on_submit():

        recruit = Recruit(
            practice_registration = practice_registration,
            user = current_user(),
            nhs_number = form.nhs_number.data,
            date_of_birth = form.date_of_birth.data,
            date_recruited = form.date_recruited.data,
            )

        db.session.add(recruit)
        db.session.commit()

        return redirect(url_for('recruits_index', code=code))

    form = RecruitNewForm(code = code)

    return render_template('practices/recruits/edit.html', form=form, practice_registration=practice_registration)

@app.route('/practices/<string:code>/recruits/<int:id>/edit', methods=['GET','POST'])
def recruits_edit(code, id):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()
    recruit = Recruit.query.get(id)

    form = RecruitEditForm()

    if form.validate_on_submit():

        recruit.nhs_number = form.nhs_number.data
        recruit.date_of_birth = form.date_of_birth.data
        recruit.date_recruited = form.date_recruited.data

        db.session.commit()

        return redirect(url_for('recruits_index', code=code))

    form = RecruitEditForm(obj=recruit)

    return render_template('practices/recruits/edit.html', form=form, practice_registration=practice_registration)

def current_user():
    return User.query.filter(User.username == 'richard').first()
