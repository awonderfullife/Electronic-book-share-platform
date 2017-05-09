# -*- coding: utf-8 -*-

import time

from flask import Flask, flash, render_template, request, session,jsonify
from flask import send_from_directory
from werkzeug.security import generate_password_hash
from config import *
from dataBaseSupport import JSONProvider,SQLProvider
from emailSupport import send_mail
from user import User, TempUser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

database = SQLProvider()


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


@app.route("/download/<path:filename>")
def download(filename):
    dirpath = os.path.join(app.root_path, 'static\Ebook')
    return send_from_directory(dirpath, filename, as_attachment=True)


@app.route('/item/')
@app.route('/item/<name>')
def hello(name=None):
    return render_template('item.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    post_id = unicode(request.form['id'])
    post_password = unicode(request.form['password'])

    user = User(post_id)
    result = user.verify_password(post_password)

    if result:
        session['logged_in'] = True
        session['user'] = user.to_dict()
    else:
        flash('wrong password!')
    return index()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route("/register", methods=['GET', 'POST'])
def register():
    post_id = unicode(request.form['id'])
    post_password = unicode(request.form['password'])
    post_username = unicode(request.form['username'])

    if database.get_name_by_id(post_id) is None:
        vid = generate_password_hash(post_id)
        t_user = TempUser(vid)
        t_user.user_info = [post_id, post_username, None, int(time.time())]
        t_user.set_password(post_password)
        t_user.add_user()

        url = 'Here is an email for you:\n' + unicode(
            LOCAL_HOST) + ':' + unicode(
            PORT) + \
              '/verify/' + unicode(vid)
        send_mail(EMAIL_ADDRESS_ADMIN, post_id, EMAIL_SUBJECT_REGISTER, url)
        return render_template('success.html')
    else:
        return "User already registered"


@app.route('/verify/<vid>')
def verify(vid=None):
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
                session['user'] = new_user.to_dict()
                user_dict = new_user.to_dict()
                return render_template('register_complete.html', username=
                user_dict['username'])
            else:
                return "Out of Date"
        except KeyError:
            return "Invalid User ID"
    return "404"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('welcome.html')
    else:
        return render_template('main.html', user=session.get('user'))

@app.route('/api/v1/user', methods=['GET', 'POST'])
def users():
    if session.get('logged_in') is True:
        if request.method == 'GET':
            user = database.getUserInfo(session['email'])  #user [username, userid, userphone,userscore]
            if user:
                user_json = {}
                user_json["name"] = user[0]
                user_json["email"] = user[1]
                user_json["phone"] = user[2]
                user_json["score"] = user[3]
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
            book = database.getEBookInfo(book_id)  #book [bookname, booktype, booknotes]
            if book:
                book_json = {}
                book_json["name"] = book[0]
                book_json["score"] = 0
                book_json["rate"] = 0
                book_json["description"] = book[2]
                book_json["download_time"] = 0
                book_json["author"] = ""
                book_json["catagory"] = book[1]
                book_json["img_url"] = ""
                book_json["uploader"] = ""
                book_json["created_at"] = ""
                book_json["updated_at"] = ""
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

@app.route('/api/v1/download_verify', methods=['GET'])
def download_verify():
    if session.get('logged_in') is True:
        user = database.getUserInfo(session['email'])  #user [username, userid, userphone,userscore]
        book_id = request.args.get('id')
        book = database.getEBookInfo(book_id)  #book [bookname, booktype, booknotes]
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
        book_list = database.filterEbook(name,catagory,sortby,score_low,score_high,page)
        book_list_json = {}
        book_list_json["book"] = []
        for book in book_list:
            book_json = {}
            book_json["name"] = book[0]
            book_json["score"] = 0
            book_json["id"] = ""
            book_json["img_url"] = ""
            book_json["uploader"] = ""
            book_json["created_at"] = ""
            book_json["updated_at"] = ""
            book_list_json["book"].append(book_json)
        return jsonify(book_list_json)
    return 'not logged in', 400

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
