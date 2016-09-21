import datetime
from portal import db

class Practice(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.date_created = datetime.datetime.now()
