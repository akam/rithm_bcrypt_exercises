from flask import redirect, render_template, request, url_for, Blueprint, flash, session
from project.users.forms import UserForm, EditForm
from project.users.models import User
from project import db,bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)


def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash("Not Authorized")
            return redirect(url_for('users.welcome'))
        return fn(*args, **kwargs)
    return wrapper

@users_blueprint.route('/signup', methods=['GET','POST'])
def signup():
    form = UserForm(request.form)
    if form.validate_on_submit():
        try:
            user = User(form.data['username'], form.data['password'])
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            flash("Username already taken.")
            return render_template('signup.html', form=form)
        flash("Sign up successful!")
        login_user(user)
        return redirect(url_for('users.welcome'))
    return render_template('signup.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data['username']).first()
        if user and bcrypt.check_password_hash(user.password, form.data['password']):
            login_user(user)
            flash("You have successfully logged in as {}".format(user.username))
            return redirect(url_for('users.welcome'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@users_blueprint.route('/welcome')
@login_required
def welcome():
    user = User.query.get(current_user.id)
    return render_template('welcome.html', user=user)

@users_blueprint.route('/logout')
def logout():
    flash('logged out!')
    logout_user()
    return redirect(url_for('users.login'))


@users_blueprint.route('/<int:id>', methods=["GET", "PATCH", "DELETE"])
@login_required
@ensure_correct_user
def show(id):
    user = User.query.get_or_404(id)
    form = EditForm(request.form)
    if request.method == b'PATCH':
        if form.validate():
            user.username = form.data['username']
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users.show', id=user.id))
        return render_template('edit.html', user=user, form=form)
    if request.method == b'DELETE':
        db.session.delete(user)
        db.session.commit()
        flash('Deleted user')
        logout_user()
        return redirect(url_for('users.login'))
    return render_template('show.html', user=user)

@users_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    return render_template('edit.html', user=user, form=form)



