from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from portal.config import BaseConfig
from flask_wtf.csrf import CsrfProtect
from flask_security import Security, SQLAlchemyUserDatastore
import logging
import traceback

app = Flask(__name__)
app.config.from_object(BaseConfig)
CsrfProtect(app)

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(app.config['SMTP_SERVER'],
                               app.config['APPLICATION_EMAIL_ADDRESSES'],
                               app.config['ADMIN_EMAIL_ADDRESSES'],
                               app.config['ERROR_EMAIL_SUBJECT'])
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

@app.errorhandler(500)
@app.errorhandler(Exception)
def internal_error(exception):
    print(traceback.format_exc())
    app.logger.error(traceback.format_exc())
    return render_template('500.html'), 500

# Set up database
db = SQLAlchemy(app)

import portal.database
database.init_db()

from portal.models import *

@app.before_first_request
def init_security():
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    admin_role = user_datastore.find_or_create_role(name=Role.ADMIN_ROLENAME, description='Administration')

    if (not user_datastore.get_user('richard.a.bramley@uhl-tr.nhs.uk')):
      richard = user_datastore.create_user(email='richard.a.bramley@uhl-tr.nhs.uk', password='genvasc', first_name='Richard', last_name='Bramley')
      user_datastore.activate_user(richard)
      user_datastore.add_role_to_user(richard, admin_role)
      db.session.commit()

    if (not user_datastore.get_user('lcbruit@uhl-tr.nhs.uk')):
      user_datastore.create_user(email='lcbruit@uhl-tr.nhs.uk', password='iuhiuhiwuheicwiew', first_name='System', last_name='User')
      db.session.commit()

    if (not user_datastore.get_user('user@practice.nhs.uk')):
      practice = PracticeRegistration.query.filter(PracticeRegistration.code == 'C82072').first()
      if practice:
        practice_user = user_datastore.create_user(email='user@practice.nhs.uk', password='genvasc', first_name='practice', last_name='User')
        user_datastore.activate_user(practice_user)
        practice_user.practices.append(practice)
        db.session.commit()

from portal.views import *