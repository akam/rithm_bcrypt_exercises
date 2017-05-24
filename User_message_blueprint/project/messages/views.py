from flask import redirect, render_template, request, url_for, Blueprint
from project.messages.models import Message
from project.users.models import User
from project.messages.forms import MessageForm
from project import db

messages_blueprint = Blueprint(
    'messages',
    __name__,
    template_folder='templates'
)

@messages_blueprint.route('/', methods =["GET", "POST"])
def index(id):
	if request.method == "POST":
		form = MessageForm()
		if form.validate():
			new_message = Message(request.form['message'], id)
			db.session.add(new_message)
			db.session.commit()
			return redirect(url_for('messages.index',id=id))
		return render_template('messages/new.html', form=form)
	return render_template('messages/index.html', user=User.query.get(id), messages=User.query.get(id).messages)

@messages_blueprint.route('/new')
def new(id):
	user = User.query.get(id)
	form = MessageForm()
	return render_template('messages/new.html', form=form, user=user)

@messages_blueprint.route('/<int:mid>/edit')
def edit(id,mid):
	user = User.query.get(id)
	message=Message.query.get(mid)
	form = MessageForm(obj=message)
	return render_template('messages/edit.html', form=form, message=message, user=user)

@messages_blueprint.route('/<int:mid>', methods =["GET", "PATCH", "DELETE"])
def show(id,mid):
	user = User.query.get(id)
	found_message = Message.query.get(mid)
	if request.method == b"PATCH":
		form = MessageForm(request.form)
		if form.validate():
			found_message.message = request.form['message']
			db.session.add(found_message)
			db.session.commit()
			return redirect(url_for('messages.index', id=id))
		return render_template('messages/edit.html', form=form, message=found_message)
	if request.method == b"DELETE":
		db.session.delete(found_message)
		db.session.commit()
		return redirect(url_for('messages.index', id=id))
	return render_template('messages/show.html', message=found_message, user=user)


