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

def current_user():
    return User.query.filter(User.username == 'richard').first()
