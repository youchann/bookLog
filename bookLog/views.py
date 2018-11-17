from functools import wraps
from collections import OrderedDict
from flask import request, redirect, url_for, render_template, flash, abort, \
        jsonify, session, g
import os
import requests
import lepl.apps.rfc3696
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
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_view


# routeで追加したendpointの前に呼ばれる
@app.before_request
def load_user():
    user = session.get('user')
    auth = firebase.auth()
    if user is None:
        g.user = None
    else:
        g.user = auth.refresh(user['refreshToken'])


@app.route('/')
@login_required
def show_entries():
    bookId = []
    # ログインユーザーのuser_idを代入
    uid = g.user.get('userId')

    # ユーザーIDに対応するデータを取得
    userData = db.child('users_books').child(uid).get(g.user['idToken'])
    dataList = userData.val()

    # 取得したデータを配列に挿入
    if dataList != None:
        for key, val in dataList.items():
            bookId.append(val['book_id'])

    return render_template('show_entries.html',bookId=bookId) 

@app.route('/search')
@login_required
def search_books():

    return render_template('search_books.html')

@app.route('/add/<string:book_id>')
@login_required
def add_entry(book_id):
    # ログインユーザーのuser_idを代入
    uid = g.user.get('userId')

    # データベースの更新
    db.child('users_books').child(uid).push({'book_id': book_id}, g.user['idToken'])

    return redirect(url_for('show_entries'))

@app.route('/delete/<string:book_id>')
@login_required
def delete_entry(book_id):
    # ログインユーザーのuser_idを代入
    uid = g.user.get('userId')
    # データベースの更新
    userData = db.child('users_books').child(uid).get(g.user['idToken'])
    dataList = userData.val()
    for key, val in dataList.items():
        if val['book_id'] == book_id:
            db.child('users_books').child(uid).child(key).remove(g.user['idToken'])
            break
    return redirect(url_for('show_entries'))

@app.route('/create/', methods=['GET', 'POST'])
def create_user():
    auth = firebase.auth()
    email_validator = lepl.apps.rfc3696.Email()

    # ユーザー作成処理
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #バリデーションを行う
        if email_validator(email) and len(password) >= 6:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                session['user'] = user

                flash('Welcome to bookLog!!')
                return redirect(url_for('show_entries', firebase=firebase))
            except:
                flash('Error')
        else:
            flash('Please fill correctly the input form')


    return render_template('create_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
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
