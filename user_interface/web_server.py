# -*- coding: utf-8 -*-

import time
import random
from flask import Flask, flash, render_template, request, session,jsonify,abort
from flask import send_from_directory
from werkzeug.security import generate_password_hash
from config import *
from dataBaseSupport import JSONProvider,SQLProvider
from emailSupport import send_mail
from user import User, TempUser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

database = SQLProvider()

class DataBase(object):
    def __init__(self):
        self.users = {
            'admin@sjtu.edu.cn': {
                'username': 'admin',
                'password': '123456',
                'score': 1000000,
            }
        }
        self.lists = [
            {
                'url': '/book/1',
                'img_url': '/static/image/book_1.jpg',
                'name': '《数据结构：思想与实现》',
                'description': '本书条理清晰，严格按照线性结构、树形结构、集合结构和图形结构的次序来组织编写...',
                'score': 100,
                'download_times': 999,
            },
            {
                'url': '/book/2',
                'img_url': '/static/image/book_2.jpg',
                'name': '《数学分析（Ⅰ）》',
                'description': '本书是为贯彻教育部教学改革精神，实施全英语授课需要而编写，此书书稿在实际教学...',
                'score': 100,
                'download_times': 999,
            },
            {
                'url': '/book/3',
                'img_url': '/static/image/book_3.jpg',
                'name': '《面向对象软件工程：使用UML、模式与Java》',
                'description': '本书是为...',
                'score': 100,
                'download_times': 999,
            },
        ]
        self.books = {
            1: {
                'name': '《数据结构：思想与实现》',
                'score': 100,
                'rate': 5,
                'download_times': 3,
                'description': '《数据结构：思想与实现/“十二五”普通高等教育本科规划教材》条理清晰，严格按照线性结构、 树形结构、集合结构和图形结构的次序来组织编写。除了常规的数据结构内容之外，还介绍了一些 高级的数据结构，如红黑树、AA树和跳表等，并提供了大量的数据结构应用实例。让读者在学习数 据结构的同时，逐步了解为什么要学习数据结构，了解数据结构对计算机专业的重要性。《数据结 构：思想与实现/“十二五”普通高等教育本科规划教材》内容翔实，既注重数据结构和算法的原理 ，又十分强调和程序设计课程的衔接。在讲授数据结构的同时，不断加强学生对程序设计的理解。 书中的算法都有完整的C＋＋实现。这些程序结构清晰，构思精巧。',
                'author': 'jian cao',
                'catagory': 'computer science',
                'img_url': '/static/image/book_1.jpg',
                'uploader': '张老师',
                'created_at': '2017-05-06T13:28:03',
                'updated_at': '2017-05-07T07:47:03',
            },
            2: {
                'name': '《数学分析（Ⅰ）》',
                'score': 100,
                'rate': 5,
                'download_times': 4,
                'description': '《数据结构：思想与实现/“十二五”普通高等教育本科规划教材》条理清晰，严格按照线性结构、 树形结构、集合结构和图形结构的次序来组织编写。除了常规的数据结构内容之外，还介绍了一些 高级的数据结构，如红黑树、AA树和跳表等，并提供了大量的数据结构应用实例。让读者在学习数 据结构的同时，逐步了解为什么要学习数据结构，了解数据结构对计算机专业的重要性。《数据结 构：思想与实现/“十二五”普通高等教育本科规划教材》内容翔实，既注重数据结构和算法的原理 ，又十分强调和程序设计课程的衔接。在讲授数据结构的同时，不断加强学生对程序设计的理解。 书中的算法都有完整的C＋＋实现。这些程序结构清晰，构思精巧。',
                'author': 'jian cao',
                'catagory': 'computer science',
                'img_url': '/static/image/book_2.jpg',
                'uploader': '胡老板',
                'created_at': '2017-05-06T13:28:03',
                'updated_at': '2017-05-07T07:47:03',
            },
            3: {
                'name': '《面向对象软件工程：使用UML、模式与Java》',
                'score': 100,
                'rate': 5,
                'download_times': 5,
                'description': '《数据结构：思想与实现/“十二五”普通高等教育本科规划教材》条理清晰，严格按照线性结构、 树形结构、集合结构和图形结构的次序来组织编写。除了常规的数据结构内容之外，还介绍了一些 高级的数据结构，如红黑树、AA树和跳表等，并提供了大量的数据结构应用实例。让读者在学习数 据结构的同时，逐步了解为什么要学习数据结构，了解数据结构对计算机专业的重要性。《数据结 构：思想与实现/“十二五”普通高等教育本科规划教材》内容翔实，既注重数据结构和算法的原理 ，又十分强调和程序设计课程的衔接。在讲授数据结构的同时，不断加强学生对程序设计的理解。 书中的算法都有完整的C＋＋实现。这些程序结构清晰，构思精巧。',
                'author': 'jian cao',
                'catagory': 'computer science',
                'img_url': '/static/image/book_3.jpg',
                'uploader': '胡老板',
                'created_at': '2017-05-06T13:28:03',
                'updated_at': '2017-05-07T07:47:03',
            },
        }
        self.user_purchased = []
        self.user_favored = []

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

    def query_user(self, id):
        user = self.users.get(id)
        if user:
            user = user.copy()
            user.pop('password')
            return user

    def update_user(self, id, username):
        user = self.users.get(id)
        if user:
            user['username'] = username
            return True
        return False

    def book_by_id(self, id):
        return self.books.get(id)

    def update_by_id(self, id, name):
        self.users[id]['name'] = name

    def hot_books(self, num):
        return [random.choice(self.lists) for _ in range(num)]

    def user_purchase_ebook(self, user_id, ebook_id):
        self.books[ebook_id]['download_times'] += 1
        score = self.books[ebook_id]['score']
        self.users[user_id]['score'] -= score
        self.user_purchased.append((user_id, ebook_id))

    def user_ebook_access(self, user_id, ebook_id):
        for (uid, bid) in self.user_purchased:
            print uid, user_id, bid, ebook_id
            if uid == user_id and bid == ebook_id:
                return True
        return False

    def ebook_filename(self, ebook_id):
        return 'test.txt'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = werkzeug.secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html')
    return render_template('upload.html')

@app.route('/item/')
@app.route('/item/<name>')
def hello(name=None):
    return render_template('item.html', name=name)

@app.route('/book/<id>')
def book_page(id):
    return render_template('book.html')


@app.route('/list')
def book_list():
    return render_template('list.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    post_id = unicode(request.form['email'])
    post_password = unicode(request.form['password'])

    user = User(post_id)
    result = user.verify_password(post_password)
    print result

    if result:
        session['logged_in'] = True
        session['email'] = post_id
        return 'login success'
    else:
        return 'wrong password', 400



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route("/register", methods=['GET', 'POST'])
def register():
    post_id = unicode(request.form['email'])
    post_password = unicode(request.form['password'])
    post_username = unicode(request.form['username'])

    if database.get_name_by_id(post_id) is None:
        vid = generate_password_hash(post_id)
        t_user = TempUser(vid)
        t_user.user_info = [post_id, post_username, None, int(time.time())]
        t_user.set_password(post_password)
        t_user.add_user()

        url = 'Here is an email for you:\n' + unicode(LOCAL_HOST) \
              + ':' + unicode(PORT) + '/verify/' + unicode(vid)
        send_mail(EMAIL_ADDRESS_ADMIN, post_id, EMAIL_SUBJECT_REGISTER, url)
        return "register success"
    else:
        return 'email is used',400


@app.route('/verify/<vid>')
def verify(vid=None):
    print vid
    if vid is not None:
        if database.get_temp_user(vid) is None:
            return "404"
        try:
            t_user = TempUser(vid)
            if t_user.check_user_existence() is not None:
                return "User Already Exists"

            if t_user.validate_time(time.time()):
                new_user = t_user.to_real_user()
                session['logged_in'] = True
                session['mail'] = new_user.id
                return render_template('register_complete.html', username=
                new_user.username)
            else:
                return "Out of Date"
        except KeyError:
            return "Invalid User ID"
    return "404"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# @app.route('/')
# @app.route('/index')
# def index():
#     if not session.get('logged_in'):
#         return render_template('welcome.html')
#     else:
#         return render_template('main.html', user=session.get('user'))

@app.route('/api/v1/hotbooks', methods=['GET'])
def hot_books():
    num = request.args.get('num')
    books = db.hot_books(int(num))
    return jsonify(books)



@app.route('/download/<string:book_id>')
def download(book_id):
    if session.get('logged_in') is True:
        email = session['email']
        if database.checkUserEBook(email,book_id):
            dirpath = reduce(os.path.join, [app.root_path, 'static', 'Ebook'])
            filename = database.getEBookFileName(book_id)
            return send_from_directory(dirpath, filename, as_attachment=True)
        return abort(404)
    return abort(404)

@app.route('/api/v1/user', methods=['GET', 'POST'])
def users():
    if session.get('logged_in') is True:
        if request.method == 'GET':
            user = database.getUserInfo(session['email'])  #user [username, userid, userphone,userscore]
            print user
            if user:
                user_json = {user[1]:{"username": user[0], "phone": user[2],
                                      "score": user[3]}
                             }
                return jsonify(user_json)
            return 'SQL error!', 500
        elif request.method == 'POST':
            username = request.form["name"]
            phoneNum = request.form["phoneNum"]
            if database.updateUserInfo(session['email'],username,phoneNum):
                return 'update success'
            return 'update error', 500
    return 'not logged in', 400

@app.route('/api/v1/ebook', methods=['GET','POST'])
def ebook():
    if session.get('logged_in') is True:
        book_id = request.args.get('id')
        if request.method == 'GET':
            book = database.getEBookInfo(book_id)
            if book:
                book_json = {}
                book_json["name"] = book[0]
                book_json["catagory"] = book[1]
                book_json["description"] = book[2]
                book_json["score"] = book[3]
                book_json["rate"] = book[4]
                book_json["download_times"] = book[5]
                book_json["author"] = book[6]
                book_json["img_url"] = book[7]
                book_json["uploader"] = book[8]
                book_json["created_at"] = book[9]
                book_json["updated_at"] = book[10]
                return jsonify(book_json)
            return 'SQL error!', 500
        elif request.method == 'POST':
            name = request.form["name"]
            catagory = request.form["catagory"]
            score = request.form["score"]
            if database.updateEBookInfo(book_id,name,catagory,score):
                return 'update success'
            return 'update error',500
    return 'not logged in',400

@app.route('/api/v1/purchase_verify', methods=['GET'])
def download_verify():
    if session.get('logged_in') is True:
        user = database.getUserInfo(session['email'])  #user [username, userid, userphone,userscore]
        book_id = request.args.get('id')
        book = database.getEBookInfo(book_id)
        result = jsonify({'current_score': user[3]})
        if (user[3] >= book[3]):
            return result
        return result, 500
    return 'not logged in', 400

@app.route('/api/v1/list', methods=['GET'])
def List():
    if session.get('logged_in') is True:
        name = request.args.get('name')
        catagory = request.args.get('catagory')
        sortby = request.args.get('sortby')
        score_low = request.args.get('score_low')
        score_high = request.args.get('score_high')
        page = request.args.get('page')
        bookid_list = database.filterEbook(name,catagory,sortby,score_low,score_high,page)
        book_list_json = {}
        book_list_json["book"] = []
        for book_id in bookid_list:
            book = database.getEBookInfo2(book_id)
            book_json = {}
            book_json["name"] = book[0]
            book_json["score"] = book[1]
            book_json["id"] = book[2]
            book_json["img_url"] = book[3]
            book_json["uploader"] = book[4]
            book_json["created_at"] = book[5]
            book_json["updated_at"] = book[6]
            book_list_json["book"].append(book_json)
        return jsonify(book_list_json)
    return 'not logged in', 400


@app.route('/api/v1/purchase', methods=['GET'])
def purchase():
    if session.get('logged_in') is True:
        email = session['email']
        user = database.getUserInfo(email)  #user [username, userid, userphone,userscore]
        book_id = request.args.get('id')
        book = database.getEBookInfo(book_id)
        result = jsonify({'current_score': user['score']})
        if (user[3] >= book[3]):
            database.addUserRBook(email,book_id)
            database.modifyEBookDlTimes(book_id,book[5] + 1)
            database.modifyUserScore(email,user[3] - book[3])
            return result
        return result, 500
    return 'not logged in', 400


@app.route('/api/v1/purchased')
def purchased():
    result = {'purchased': False}
    if session.get('logged_in') is True:
        email = session['email']
        book_id = request.args.get('id')
        if database.checkUserEBook(email,book_id):
            result['purchased'] = True
    return jsonify(result)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    db = DataBase()
    app.run(debug=True,host='localhost', port=PORT)
