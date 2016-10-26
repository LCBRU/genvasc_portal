import datetime
from portal import app
from functools import wraps
from flask import request, render_template, flash, redirect, url_for

@app.template_filter('datetime_format')
def datetime_format(value):
    return value.strftime('%c')

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

def must_exist(model, field, request_field, error_redirect=None, message=u'The value does not exist.'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            count = model.query.filter(field == request.view_args.get(request_field)).count()

            if count == 0:
                flash("{0}: ({1} = '{2}')".format(message, request_field, request.view_args.get(request_field)), 'error')
                return redirect(url_for(error_redirect) or url_for('index'))

            return f(*args, **kwargs)

        return decorated_function
    return decorator
