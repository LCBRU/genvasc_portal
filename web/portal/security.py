from portal import app, db
from portal.models import *
from flask_security import Security, SQLAlchemyUserDatastore

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