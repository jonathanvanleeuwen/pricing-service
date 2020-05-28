from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from models.user import User, UserErrors
from models.user import requires_login
# from models.user.user import User
# import models.user.errors as UserErrors

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=["GET", "POST"])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email
            return redirect(url_for('alerts.index'))
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')


@user_blueprint.route('/login', methods=["GET", "POST"])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('alerts.index'))
        except UserErrors.UserError as e:
            flash(e.message, 'danger')
            return render_template('users/login.html')

    return render_template('users/login.html')

@user_blueprint.route('/logout')
@requires_login
def logout():
    session['email'] = None
    return render_template('users/login.html')
