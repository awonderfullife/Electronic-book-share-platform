# coding: utf-8
import os
import random
from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)


class DataBase(object):
    def __init__(self):
        self.users = {
            'admin@sjtu.edu.cn': {
                'username': 'admin',
                'password': '123456',
            }
        }
        self.lists = [
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
        ]
        self.books = {
            1: {
                "name": "《数据结构：思想与实现》",
                "score": 100,
                "rate": 5,
                "download_time": 999,
                "description": "《数据结构：思想与实现/“十二五”普通高等教育本科规划教材》条理清晰，严格按照线性结构、 树形结构、集合结构和图形结构的次序来组织编写。除了常规的数据结构内容之外，还介绍了一些 高级的数据结构，如红黑树、AA树和跳表等，并提供了大量的数据结构应用实例。让读者在学习数 据结构的同时，逐步了解为什么要学习数据结构，了解数据结构对计算机专业的重要性。《数据结 构：思想与实现/“十二五”普通高等教育本科规划教材》内容翔实，既注重数据结构和算法的原理 ，又十分强调和程序设计课程的衔接。在讲授数据结构的同时，不断加强学生对程序设计的理解。 书中的算法都有完整的C＋＋实现。这些程序结构清晰，构思精巧。",
                "author": "jian cao",
                "catagory": "computer science",
                "img_url": "/static/image/book_1.jpg",
                "uploader": "张老师",
                "created_at": "2017-05-06T13:28:03",
                "updated_at": "2017-05-07T07:47:03",
            },
            2: {
                "name": "《数学分析（Ⅰ）》",
                "score": 100,
                "rate": 5,
                "download_time": 999,
                "description": "《数据结构：思想与实现/“十二五”普通高等教育本科规划教材》条理清晰，严格按照线性结构、 树形结构、集合结构和图形结构的次序来组织编写。除了常规的数据结构内容之外，还介绍了一些 高级的数据结构，如红黑树、AA树和跳表等，并提供了大量的数据结构应用实例。让读者在学习数 据结构的同时，逐步了解为什么要学习数据结构，了解数据结构对计算机专业的重要性。《数据结 构：思想与实现/“十二五”普通高等教育本科规划教材》内容翔实，既注重数据结构和算法的原理 ，又十分强调和程序设计课程的衔接。在讲授数据结构的同时，不断加强学生对程序设计的理解。 书中的算法都有完整的C＋＋实现。这些程序结构清晰，构思精巧。",
                "author": "jian cao",
                "catagory": "computer science",
                "img_url": "/static/image/book_2.jpg",
                "uploader": "胡老板",
                "created_at": "2017-05-06T13:28:03",
                "updated_at": "2017-05-07T07:47:03",
            },
            3: {
                "name": "《面向对象软件工程：使用UML、模式与Java》",
                "score": 100,
                "rate": 5,
                "download_time": 999,
                "description": "《数据结构：思想与实现/“十二五”普通高等教育本科规划教材》条理清晰，严格按照线性结构、 树形结构、集合结构和图形结构的次序来组织编写。除了常规的数据结构内容之外，还介绍了一些 高级的数据结构，如红黑树、AA树和跳表等，并提供了大量的数据结构应用实例。让读者在学习数 据结构的同时，逐步了解为什么要学习数据结构，了解数据结构对计算机专业的重要性。《数据结 构：思想与实现/“十二五”普通高等教育本科规划教材》内容翔实，既注重数据结构和算法的原理 ，又十分强调和程序设计课程的衔接。在讲授数据结构的同时，不断加强学生对程序设计的理解。 书中的算法都有完整的C＋＋实现。这些程序结构清晰，构思精巧。",
                "author": "jian cao",
                "catagory": "computer science",
                "img_url": "/static/image/book_3.jpg",
                "uploader": "胡老板",
                "created_at": "2017-05-06T13:28:03",
                "updated_at": "2017-05-07T07:47:03",
            },
        }

    def register(self, email, username, password):
        if email in self.users:
            return False
        self.users[email] = {
            'username': username,
            'password': password,
        }
        return True

    def login_verify(self, email, password):
        user = self.users.get(email)
        if user:
            return user['password'] == password
        return False

    def query_by_id(self, id):
        return self.users.get(id)

    def book_by_id(self, id):
        return self.books.get(id)

    def update_by_id(self, id, name):
        self.users[id]['name'] = name

    def hot_books(self, num):
        return [random.choice(self.lists) for _ in range(num)]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/book/<id>')
def book_page(id):
    return render_template('book.html')


@app.route('/list')
def list():
    return render_template('list.html')


@app.route('/signup', methods=['POST'])
def register():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    if db.register(email, username, password):
        return 'register success'
    return 'email is used', 400


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if db.login_verify(email, password):
        session['logged_in'] = True
        session['email'] = email
        return 'login success'
    return 'login error', 400


@app.route('/api/v1/user', methods=['GET'])
def users():
    if session.get('logged_in') is True:
        user = db.query_by_id(session['email'])
        if user:
            return jsonify(user)
        return 'SQL error!', 500
    return 'not logged in', 400


@app.route('/api/v1/hotbooks', methods=['GET'])
def hot_books():
    num = request.args.get('num')
    books = db.hot_books(int(num))
    return jsonify(books)


@app.route('/api/v1/ebook', methods=['GET'])
def ebook():
    book_id = request.args.get('id')
    book = db.book_by_id(int(book_id))
    return jsonify(book)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    db = DataBase()
    app.run(debug=True, host='0.0.0.0', port=4000)
