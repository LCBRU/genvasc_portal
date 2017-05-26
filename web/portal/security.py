import os
import yaml
import string
import random
from portal import app, db, user_datastore
from portal.models import *

user_file_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'users.yml')


@app.before_first_request
def init_security():
    admin_role = user_datastore.find_or_create_role(
        name=Role.ADMIN_ROLENAME,
        description='Administration')

    user_file = open(user_file_path, "r")
    users = yaml.load_all(user_file)
    for user_details in users:

        user = user_datastore.get_user(user_details['email'])
        if not user:
            app.logger.info("Creating User: {}".format(user_details['email']))
            app.logger.info("Password: {}".format(get_random_password()))

            user = user_datastore.create_user(
                email=user_details['email'],
                password=get_random_password(),
                first_name=user_details['first_name'],
                last_name=user_details['last_name']
            )

        if not user_details.get('inactive', False):
            user_datastore.activate_user(user)

        if user_details.get('is_admin', False):
            user_datastore.add_role_to_user(user, admin_role)

        if user_details.get('is_admin', False):
            user_datastore.add_role_to_user(user, admin_role)

        if "practices" in user_details:

            for practice_code in user_details['practices']:
                practice = PracticeRegistration.query.filter(
                    PracticeRegistration.code == practice_code
                ).first()

                if practice:
                    user.practices.append(practice)

        db.session.commit()


def get_random_password():

    password_chars = random.sample(string.ascii_lowercase, 10)
    password_chars += random.sample(string.ascii_uppercase, 10)
    password_chars += random.sample(string.punctuation, 10)

    random.shuffle(password_chars)

    return "".join(password_chars)
