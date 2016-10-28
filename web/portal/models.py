import datetime
from portal import db

class Practice(db.Model):

    __tablename__ = 'etl_practice_details'

    id = db.Column(db.Integer)
    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    ccg_name = db.Column(db.String, nullable=False)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)

    def __init__(self, *args, **kwargs):
        self.username = kwargs.get('username')

class PracticeRegistration(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref('registrations', cascade="all, delete-orphan"))
    code = db.Column(db.String, db.ForeignKey(Practice.code))
    date_created = db.Column(db.DateTime, nullable=False)
    practice = db.relationship(Practice)
    date_initiated = db.Column(db.Date, nullable=True)
    notes = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.get('user').id
        self.code = kwargs.get('code')
        self.date_initiated = kwargs.get('date_initiated')
        self.notes = kwargs.get('notes')
        self.date_created = datetime.datetime.now()

class StaffMember(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    practice_registration_id = db.Column(db.Integer, db.ForeignKey(PracticeRegistration.id))
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    practice_registration = db.relationship(PracticeRegistration, backref=db.backref('staff', cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        self.practice_registration_id = kwargs.get('practice_registration').id
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.date_created = datetime.datetime.now()

    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

class DapsSubmission(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime, nullable=False)
    date_returned = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        self.date_submitted = datetime.datetime.now()

class Recruit(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    practice_registration_id = db.Column(db.Integer, db.ForeignKey(PracticeRegistration.id))
    practice_registration = db.relationship(PracticeRegistration, backref=db.backref('recruits', cascade="all, delete-orphan"))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref('recruits', cascade="all, delete-orphan"))
    daps_submission_id = db.Column(db.Integer, db.ForeignKey(DapsSubmission.id))
    daps_submission = db.relationship(DapsSubmission, backref=db.backref('recruits'))
    nhs_number = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    date_recruited = db.Column(db.Date, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        self.practice_registration_id = kwargs.get('practice_registration').id
        self.user_id = kwargs.get('user').id
        self.nhs_number = kwargs.get('nhs_number')
        self.date_of_birth = kwargs.get('date_of_birth')
        self.date_recruited = kwargs.get('date_recruited')
        self.date_created = datetime.datetime.now()

daps_submission_recruits = db.Table('daps_submission_recruit',
    db.Column('daps_submission_id', db.Integer, db.ForeignKey('daps_submission.id')),
    db.Column('recruit_id', db.Integer, db.ForeignKey('recriut.id'))
)

