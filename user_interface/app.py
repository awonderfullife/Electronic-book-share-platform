# coding: utf-8
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

class DataBase():
    def __init__(self):
        self.users = {'hawnzug@gmail.com': {'username': 'admin', 'password': '1234567'}}
        self.hots = [
                {
                    'url': '/book/1',
                    'img_url': '/static/image/book_1.jpg',
                    'name': '《数据结构：思想与实现》',
                    'description': '本书条理清晰，严格按照线性结构、树形结构、集合结构和图形结构的次序来组织编写...',
                    'score': 10,
                    'download_time': 999,
                },
                {
                    'url': '/book/2',
                    'img_url': '/static/image/book_2.jpg',
                    'name': '《数学分析（Ⅰ）》',
                    'description': '本书是为贯彻教育部教学改革精神，实施全英语授课需要而编写，此书书稿在实际教学...',
                    'score': 10,
                    'download_time': 999,
                },
                {
                    'url': '/book/3',
                    'img_url': '/static/image/book_3.jpg',
                    'name': '《面向对象软件工程：使用UML、模式与Java》',
                    'description': '本书是为...',
                    'score': 10,
                    'download_time': 999,
                },
                {
                    'url': '/book/2',
                    'img_url': '/static/image/book_2.jpg',
                    'name': '《数学分析（Ⅰ）》',
                    'description': '本书是为贯彻教育部教学改革精神，实施全英语授课需要而编写，此书书稿在实际教学...',
                    'score': 10,
                    'download_time': 999,
                },
                ] * 2

    def register(self, email, username, password):
        if email in self.users:
            return False
        else:
            self.users[email] = {
                    'username': username,
                    'password': password,
                    }
            return True

    def login_verify(self, email, password):
        user = self.users.get(email)
        if user:
            return user['password'] == password
        else:
            return False

    def query_by_id(self, id):
        return self.users.get(id)

    def update_by_id(self, id, name):
        self.users[id]['name'] = name

    def hot_books(self, num):
        return self.hots[:num]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/book')
def signup():
    return render_template('book.html')


@app.route('/signup', methods=['POST'])
def register():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    if db.register(email, username, password):
        return 'register success'
    else:
        return 'email is used', 400


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if db.login_verify(email, password):
        session['logged_in'] = True
        session['email'] = email
        return 'login success'
    else:
        return 'login error', 400


@app.route('/api/v1/user', methods=['GET'])
def user():
    if session.get('logged_in') == True:
        user = db.query_by_id(session['email'])
        if user:
            return jsonify(user)
        else:
            return 'SQL error!', 500
    else:
        return 'not logged in', 400


@app.route('/api/v1/hotbooks', methods=['GET'])
def hot_books():
    num = request.args.get('num')
    books = db.hot_books(int(num))
    return jsonify(books)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    db = DataBase()
    app.run(debug=True,host='0.0.0.0', port=4000)
