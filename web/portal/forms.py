import re
from datetime import date
from flask import flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, HiddenField, FormField, DecimalField, IntegerField, TextAreaField, Form as WtfForm
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.fields.html5 import DateTimeField, DateField
from wtforms_components import read_only
from wtforms.validators import ValidationError
from portal.models import *
from portal.datatypes import *

class Exists(object):
    def __init__(self, model, field, message=u'The value does not exist.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        exists = self.model.query.filter(self.field == field.data).first()
        if not exists:
            raise ValidationError(self.message)

class NotExists(object):
    def __init__(self, model, field, message=u'The value already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        exists = self.model.query.filter(self.field == field.data).first()
        if exists:
            raise ValidationError(self.message)

class DateMinAge(object):
    def __init__(self, min, message=None):
        self.min = min

        if message:
            self.message = message
        else:
            self.message = "Age cannot be less than {0}".format(min)

    def __call__(self, form, field):
        if DateHelper.age_in_years(field.data) < self.min:
            raise ValidationError(self.message)

class DateMax(object):
    def __init__(self, max, message=None):
        self.max = max

        if message:
            self.message = message
        else:
            self.message = "Cannot be after {0:%d/%m/%Y}".format(max)

    def __call__(self, form, field):
        if field.data > self.max:
            raise ValidationError(self.message)

class DateMin(object):
    def __init__(self, min, message=None):
        self.min = min

        if message:
            self.message = message
        else:
            self.message = "Cannot be before {0:%d/%m/%Y}".format(min)

    def __call__(self, form, field):
        if field.data < self.min:
            raise ValidationError(self.message)

class MinimumAgeAtRecruitment(object):
    def __init__(self, min, message=None):
        self.min = min

        if not message:
            message = "Age at recruitment cannot be less than {0}".format(min)
        self.message = message

    def __call__(self, form, field):
        if DateHelper.full_years_since(field.data, form.date_recruited.data) < self.min:
            raise ValidationError(self.message)

class MaximumAgeAtRecruitment(object):
    def __init__(self, max, message=None):
        self.max = max

        if not message:
            message = "Age at recruitment cannot be greater than {0}".format(max)
        self.message = message

    def __call__(self, form, field):
        if DateHelper.full_years_since(field.data, form.date_recruited.data) > self.max:
            raise ValidationError(self.message)

class ValidNhsNumber(object):
    def __call__(self, form, field):
        if not NhsNumberHelper.is_valid(field.data):
            raise ValidationError('NHS number is invalid')

class FlashingForm(FlaskForm):
    def validate_on_submit(self):
        result = super(FlashingForm, self).validate_on_submit()

        if not result:
            for field, errors in self.errors.items():
                for error in errors:
                    flash(u"Error in the %s field - %s" % (getattr(self, field).label.text, error), 'error')
        return result

class SearchForm(FlashingForm):
    search = StringField('Search', validators=[Length(max=20)])
    page = IntegerField('Page', default=1)

class SelectForm(FlashingForm):
    id = HiddenField('id')

class DeleteForm(FlashingForm):
    id = HiddenField('id')

class PracticeAddForm(FlashingForm):
    code = HiddenField('code', validators=[
        Exists(Practice, Practice.code, "Practice does not exist"),
        NotExists(PracticeRegistration, PracticeRegistration.code, "Practice is already registered")
        ])
    date_initiated = DateField('Date Initiated', format='%d/%m/%Y')
    notes = TextAreaField('Notes')    

class PracticeEditForm(FlashingForm):
    code = HiddenField('code', validators=[
        Exists(Practice, Practice.code, "Practice does not exist"),
        Exists(PracticeRegistration, PracticeRegistration.code, "Practice is not registered")
        ])
    date_initiated = DateField('Date Initiated', format='%d/%m/%Y')
    notes = TextAreaField('Notes')    

class StaffMemberForm(WtfForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100)])


class StaffMemberEditForm(FlashingForm):
    id = HiddenField('id', validators=[
        Exists(StaffMember, StaffMember.id, "Staff member does not exist")
        ])
    staff_member = FormField(StaffMemberForm)

class StaffMemberNewForm(FlashingForm):
    code = HiddenField('code', validators=[
        Exists(PracticeRegistration, PracticeRegistration.code, "Practice is not registered")
        ])
    staff_member = FormField(StaffMemberForm)

class RecruitNewForm(FlashingForm):
    code = HiddenField('code', validators=[
        Exists(PracticeRegistration, PracticeRegistration.code, "Practice is not registered")
        ])
    nhs_number = StringField('NHS Number', validators=[DataRequired(), Length(max=20), ValidNhsNumber()])
    date_of_birth = DateField('Date of Birth', format='%d/%m/%Y')
    date_recruited = DateField('Date Recruited', format='%d/%m/%Y')

class RecruitEditForm(FlashingForm):
    id = HiddenField('id', validators=[
        Exists(Recruit, Recruit.id, "Recruit does not exist")
        ])
    nhs_number = StringField('NHS Number', validators=[DataRequired(), Length(max=20), ValidNhsNumber()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired(), MinimumAgeAtRecruitment(40), MaximumAgeAtRecruitment(70)], format='%d/%m/%Y')
    date_recruited = DateField('Date Recruited', validators=[DateMax(date.today()), DateMin(date(2010, 1, 1))], format='%d/%m/%Y')
