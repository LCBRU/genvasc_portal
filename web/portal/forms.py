from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField, HiddenField, FormField, DecimalField, IntegerField, Form as WtfForm
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.fields.html5 import DateTimeField
from wtforms_components import read_only

class SearchForm(Form):
    search = StringField('Search', validators=[Length(max=20)])
