from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.users.models import User
from project.users.forms import UserForm, LoginForm, EditForm
from project import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)


@users_blueprint.route('/', methods =["GET", "POST"])
def index():
	if request.method == "POST":
		form = UserForm(request.form)
		if form.validate():
			new_user = User(request.form['username'],request.form['password'], request.form['email'], request.form['first_name'], request.form['last_name'])
			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for('users.index'))
		return render_template('users/new.html', form=form)
	return render_template('users/index.html', users=User.query.all())

@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data['username']).first()
        if user and bcrypt.check_password_hash(user.password, form.data['password']):
            login_user(user)
            flash("You have successfully logged in as {}".format(user.username))
            return redirect(url_for('messages.index', id=user.id))
        flash("Invalid credentials.")
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    flash('Sucessfully logged out!')
    return redirect(url_for('users.login'))


@users_blueprint.route('/new')
def new():
    form = UserForm()
    return render_template('users/new.html', form=form)

@users_blueprint.route('/<int:id>/edit')
@login_required
def edit(id):
	users=User.query.get(id)
	form = EditForm(obj=users)
	return render_template('users/edit.html', form=form, user=users)

@users_blueprint.route('/<int:id>', methods =["GET", "PATCH", "DELETE"])
@login_required
def show(id):
    found_user = User.query.get(id)
    if request.method == b"PATCH":
        form = EditForm(request.form)
        if form.validate():
            found_user.first_name = request.form['first_name']
            found_user.last_name = request.form['last_name']
            found_user.email = request.form['email']
            found_user.username = request.form['username']
            db.session.add(found_user)
            db.session.commit()
            return redirect(url_for('users.show', id=found_user.id))
        return render_template('users/edit.html', form=form, user=found_user)
    if request.method == b"DELETE":
        db.session.delete(found_user)
        db.session.commit()
        return redirect(url_for('users.index'))
    return render_template('users/show.html', user=found_user)





