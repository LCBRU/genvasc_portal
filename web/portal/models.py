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

class PracticeRegistration(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, db.ForeignKey(Practice.code))
    date_created = db.Column(db.DateTime, nullable=False)
    practice = db.relationship(Practice)

    def __init__(self, code):
        self.code = code
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

