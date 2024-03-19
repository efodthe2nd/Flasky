from flask import Flask, render_template, session, redirect, url_for
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email


app = Flask(__name__)


@main.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate.on_submit():
    user=User.query.filter_by(username=form.name.data).first()
    if user is None:
      user = User(username=form.name.data)
      db.session.add(user)
      db.session.commit()
      session['known'] = False
      if app.config['FLASKY_ADMIN']:
        send_email(app.config['FLASKY_ADMIN'],'New User', 'mail/new_user', user=user)
    else:
      session['known'] = True
    session['name'] = form.name.data
    form.name.data = ""
    return redirect(url_for('.index'))
  return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name)