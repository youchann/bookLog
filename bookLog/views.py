from functools import wraps
from flask import request, redirect, url_for, render_template, flash, abort, \
        jsonify, session, g
from bookLog import app
from bookLog.config import fireConfig
import pyrebase
import firebase_admin
# from bookLog.models import Entry

# ログインしているかを判断するデコレータ
def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            # return redirect(url_for('login', next=request.path))
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_view


# routeで追加したendpointの前に呼ばれる
@app.before_request
def load_user():
    user = session.get('user')
    if user is None:
        g.user = None
    else:
        # g.user = User.query.get(session['user'])
        g.user = user


@app.route('/')
@login_required
def show_entries():
    # entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template('show_entries.html')
#
# @app.route('/add', methods=['POST'])
# def add_entry():
#     entry = Entry(
#             title=request.form['title'],
#             text=request.form['text']
#             )
#     db.session.add(entry)
#     db.session.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))
#
#
# @app.route('/users/')
# def user_list():
#     return 'list users'
#
# @app.route('/users/<int:user>/')
# def user_detail(user):
#     return 'detail user ' + str(user)
#
# @app.route('/users/<int:user>/edit/', methods=['GET', 'POST'])
# def user_edit(user):
#     return 'edit user ' + str(user)
#
# @app.route('/users/create/', methods=['GET', 'POST'])
# def user_create():
#     return 'create a new user'
#
# @app.route('/users/<int:user>/delete/', methods=['DELETE'])
# def user_delete(user):
#     return NotImplementedError('DELETE')


@app.route('/login', methods=['GET', 'POST'])
def login():

    firebase = pyrebase.initialize_app(fireConfig)
    auth = firebase.auth()
    # user = auth.sign_in_with_email_and_password(email, password)
    # session[user] = user

    # ログイン処理
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            flash('You were logged in')
            session['user'] = user
            print(session['user'])
            return redirect(url_for('show_entries'))
        except:
            flash('Invalid email or password')

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))
