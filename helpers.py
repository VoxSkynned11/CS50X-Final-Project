from functools import wraps
from flask import g, request, redirect, url_for, session


"""https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/"""
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/secret")
        return f(*args, **kwargs)
    return decorated_function