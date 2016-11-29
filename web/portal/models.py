import datetime, uuid
from portal import db

class Practice(db.Model):

    __tablename__ = 'etl_practice'

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)

    def __init__(self, *args, **kwargs):
        self.username = kwargs.get('username')

class PracticeRegistration(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, db.ForeignKey(Practice.code))
    date_created = db.Column(db.DateTime, nullable=False)
    practice = db.relationship(Practice)

    def __init__(self, *args, **kwargs):
        self.code = kwargs.get('code')
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

class Recruit(db.Model):

    id = db.Column(db.String(50), primary_key=True)
    source_system = db.Column(db.String(50), nullable=False)
    practice_registration_id = db.Column(db.Integer, db.ForeignKey(PracticeRegistration.id))
    practice_registration = db.relationship(PracticeRegistration, backref=db.backref('recruits', cascade="all, delete-orphan"))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref('recruits', cascade="all, delete-orphan"))
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
        self.id = uuid.uuid1()
        self.source_system = 'PORTAL'

    @property
    def date_of_birth_day(self):
        return self.date_of_birth.day

    @property
    def date_of_birth_month(self):
        return self.date_of_birth.month

    @property
    def date_of_birth_year(self):
        return self.date_of_birth.year

    def is_portal_created(self):
        return self.source_system == 'PORTAL'

class RecruitStatus(db.Model):

    __tablename__ = 'etl_recruit_status'

    id = db.Column(db.String(50), db.ForeignKey(Recruit.id), primary_key=True)
    status = db.Column(db.String(100))
    study_id = db.Column(db.String(100))
    processed_by = db.Column(db.String(500))

