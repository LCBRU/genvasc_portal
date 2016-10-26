from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func
from portal import app, db
from portal.models import *
from portal.forms import *
from portal.helpers import *

@app.route('/practices/<string:code>/staff')
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def staff_index(code):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    searchForm = SearchForm(formdata = request.args)

    q = StaffMember.query.join(PracticeRegistration, StaffMember.practice_registration).filter(PracticeRegistration.code == code)

    if searchForm.search.data:
        q = q.filter(func.concat(StaffMember.first_name, ' ', StaffMember.last_name).like("%{}%".format(searchForm.search.data)))

    staff = (
        q.order_by(StaffMember.last_name.asc(), StaffMember.first_name.asc())
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False))

    return render_template('practices/staff/index.html', staff=staff, practice_registration=practice_registration, searchForm=searchForm)

@app.route('/practices/<string:code>/staff/add', methods=['GET','POST'])
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def staff_add(code):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    form = StaffMemberNewForm()

    if form.validate_on_submit():

        staff_member = StaffMember(
            practice_registration = practice_registration,
            first_name = form.staff_member.first_name.data,
            last_name = form.staff_member.last_name.data

            )

        db.session.add(staff_member)
        db.session.commit()

        return redirect(url_for('staff_index', code=code))

    form = StaffMemberNewForm(code = code)

    return render_template('practices/staff/edit.html', form=form, practice_registration=practice_registration)

@app.route('/practices/<string:code>/staff/<int:id>/edit', methods=['GET','POST'])
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
@must_exist(model=StaffMember, field=StaffMember.id, request_field='id', error_redirect='practices_index', message="Staff member does not exist")
def staff_edit(code, id):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()
    staff_member = StaffMember.query.get(id)

    form = StaffMemberEditForm()

    if form.validate_on_submit():

        staff_member.first_name = form.staff_member.first_name.data
        staff_member.last_name = form.staff_member.last_name.data

        db.session.commit()

        return redirect(url_for('staff_index', code=code))

    form = StaffMemberEditForm(id=id, staff_member=staff_member)

    return render_template('practices/staff/edit.html', form=form, practice_registration=practice_registration)

@app.route('/practices/<string:code>/staff/<int:id>/delete')
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
@must_exist(model=StaffMember, field=StaffMember.id, request_field='id', error_redirect='practices_index', message="Staff member does not exist")
def staff_delete(code, id):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()
    staff_member = StaffMember.query.get(id)
    form = DeleteForm(obj=staff_member)
    return render_template('practices/staff/delete.html', form=form, staff_member=staff_member, practice_registration=practice_registration)

@app.route('/practices/<string:code>/staff/<int:id>/delete', methods=['POST'])
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def staff_delete_confirm(code, id):
    form = DeleteForm()

    if form.validate_on_submit():
        staff_member = StaffMember.query.get(form.id.data)

        if (staff_member):
            db.session.delete(staff_member)
            db.session.commit()
            flash("Deleted staff member {}.".format(staff_member.full_name()))
            
    return redirect(url_for('staff_index', code=code))