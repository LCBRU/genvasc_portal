from flask import redirect, url_for
from portal import app

@app.route('/', methods=['GET'])
def index():
	return redirect(url_for('practices_index', _external=True, _scheme="https"))
