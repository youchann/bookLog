from functools import wraps
from flask import request, redirect, url_for, render_template, flash, abort, \
        jsonify, session, g
import requests
from bookLog import app
import bookLog.config as config
import pyrebase

firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
url = config.google_books_api_url
db = firebase.database()


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
        g.user = user


@app.route('/')
@login_required
def show_entries():
    bookId = []
    # ログインユーザーのuidを代入
    uid = g.user.get('localId')

    # data = db.child("users_books").get(g.user['idToken'])
    userData = db.child("users_books").child(uid).get(g.user['idToken'])
    dataList = userData.val()
    del dataList[0] # 最初のNone要素を削除
    for data in dataList:
        bookId.append(data['book_id'])

    return render_template('show_entries.html',bookId=bookId) 

@app.route('/search')
@login_required
def search_books():
    
    return render_template('search_books.html') 
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
    # firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    auth = firebase.auth()

    # ログイン処理
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            flash('You were logged in')
            session['user'] = user
            return redirect(url_for('show_entries', firebase=firebase))
        except:
            flash('Invalid email or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))
