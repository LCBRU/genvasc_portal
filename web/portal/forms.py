from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, HiddenField, FormField, DecimalField, IntegerField, Form as WtfForm
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.fields.html5 import DateTimeField
from wtforms_components import read_only
from wtforms.validators import ValidationError
from portal.models import *

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

class FlashingForm(FlaskForm):
	def validate_on_submit(self):
		result = super(FlashingForm, self).validate_on_submit()

		if not result:
		    for field, errors in self.errors.items():
		        for error in errors:
		            flash((error), 'error')

		return result

class SearchForm(FlashingForm):
    search = StringField('Search', validators=[Length(max=20)])

class SelectForm(FlashingForm):
    id = HiddenField('id')

class PracticeRegisterForm(FlashingForm):
    code = HiddenField('code', validators=[
    	Exists(Practice, Practice.code, "Practice does not exist."),
    	NotExists(PracticeRegistration, PracticeRegistration.code, "Practice is already registered.")
    	])
