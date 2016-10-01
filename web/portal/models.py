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
    code = db.Column(db.String, db.ForeignKey('etl_practice_details.code'))
    date_created = db.Column(db.DateTime, nullable=False)
    practice = db.relationship("Practice")

    def __init__(self, code):
        self.code = code
        self.date_created = datetime.datetime.now()

