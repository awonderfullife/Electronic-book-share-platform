# coding: utf-8
import random
import string
from datetime import datetime

from flask import Flask, render_template, request, session, jsonify, abort
from flask import redirect, url_for
from flask import send_from_directory
from flask import json
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import *
from emailSupport import send_mail

app = Flask(__name__)

from dataBaseSupport import SQLProvider


class DataBase(object):
    def __init__(self):
        self.sql_db = SQLProvider()

    def register(self, email, username, password):
        return self.sql_db.getUserInfo(email) is None

    def register_temp_user(self, vid, email, username, password_hash):
        self.sql_db.add_temp_user(vid, [email, username, password_hash, 1000])

    def get_temp_user(self, vid):
        data = self.sql_db.get_temp_user(vid)
        if data is not None:
            return {
                'email': data[0],
                'passwd_hash': data[2],
                'username': data[1]
            }
        else:
            return None

    def remove_temp_user(self, vid):
        self.sql_db.validate_temp_user(vid)

    def login_verify(self, email, password):
        return check_password_hash(
            self.sql_db.get_password_hash(email).rstrip(' '),
            password)

    def query_user(self, id):
        info = self.sql_db.getUserInfo(id)
        if info:
            return {
                'username': info[0],
                'password': info[1],
                'score': info[3]
            }
        else:
            return None

    def add_user(self, id, username, passwd_hash):
        self.sql_db.add_user(id, username, passwd_hash)
        self.sql_db.modifyUserScore(id, 5000)

    def update_user(self, id, username):
        return self.sql_db.set_username(id, username)

    def book_by_id(self, id):
        info = self.sql_db.getEBookInfo(id)
        filename_info = self.sql_db.get_EBook_FileStoredName(id)
        return {
            'name': info[0],
            'catagory': info[1],
            'description': info[2],
            'score': info[3],
            'rate': info[4],
            'download_times': info[5],
            'author': info[6],
            'img_url': info[7],
            'uploader': info[8],
            'filename': filename_info[0],
            'storename': filename_info[1]
        }

    def update_by_id(self, id, name):
        self.sql_db.modifyEBookName(id, name)
        # self.users[id]['name'] = name

    def get_ebook_info(self, id):
        raw_result = self.sql_db.getEBookInfo(id)
        raw_result2 = self.sql_db.get_EBook_FileStoredName(id)
        if len(raw_result2) == 0:
            raw_result2 = ['test.txt','test.txt']
        return {
            'description': raw_result[2],
            'updated_at': raw_result[-1], 'download_times': raw_result[5],
                                                            'rate':
                                                                raw_result[4],
            'uploader': raw_result[-3],
            'name': raw_result[0],
            'author': raw_result[6], 'url': '/book/'+str(id),
            'created_at': raw_result[-2], 'storename': raw_result2[1],
            'filename': raw_result2[0],
            'score': raw_result[3], 'catagory': raw_result[1],
            'img_url': raw_result[-4]

        }

    def hot_books(self, num):
        ebook_id_list = random.sample(self.sql_db.filterEbook(),num)
        res = []
        for id in ebook_id_list:
            res.append(self.get_ebook_info(id))
        return res

    def user_purchase_ebook(self, user_id, ebook_id):
        ebook_info = self.book_by_id(ebook_id)
        d_times = ebook_info['download_times']
        book_score = ebook_info['score']
        self.sql_db.modifyEBookDlTimes(ebook_id, d_times + 1)
        score = self.sql_db.getUserInfo(user_id)[3]
        self.sql_db.modifyUserScore(user_id, score - book_score)
        self.sql_db.add_user_purchased_EBook(user_id, ebook_id)

    def user_ebook_access(self, user_id, ebook_id):
        return self.sql_db.check_user_purchased_EBook(user_id, ebook_id)

    def upload_ebook(self, email, name, author, catagory,
                     description, score, storename, image_name, filename):
        book_id = ''.join(random.choice(string.ascii_uppercase +
                                        string.digits) for _ in range(6))
        while self.sql_db.getEBookInfo(book_id) is not None:
            book_id = ''.join(random.choice(string.ascii_uppercase +
                                            string.digits) for _ in range(6))


        self.sql_db.add_ebook(id=book_id,
                              name=name, score=score,
                              rate=5, download_times=0,
                              description=description, author=author,
                              category=catagory,
                              img_url='/static/image/' + image_name,
                              uploader=email,
                              created_time='2017-05-06T13:28:03',
                              updated_time='2017-05-07T07:47:03')

        self.sql_db.add_EBook_FileStoredName(EBookID=book_id,
                                             filename=filename,
                                             storedname=storename)

        self.sql_db.add_user_uploaded_EBook(email, book_id)

    def upload_list(self, email):
        id_list = self.sql_db.get_user_uploaded_EBook_list(email)
        ebook_list = list()
        for id in id_list:
            try:
                ebook_list.append(self.get_ebook_info(id))
            except TypeError:
                continue
        return ebook_list


    def purchase_list(self, email):
        id_list = self.sql_db.get_user_purchased_EBook_list(email)
        ebook_list = list()
        for id in id_list:
            try:
                ebook_list.append(self.get_ebook_info(id))
            except TypeError:
                continue
        return ebook_list

    def get_map_book_list(self,book_type):
        if book_type=='cs':
            book_id_list = self.sql_db.filterEbook(catagory='计算机')

            book_list=[]
            for book_id in book_id_list:
                book_info = self.get_ebook_info(book_id)
                book_list.append(
                    {
                        'name':book_info['name'],
                        'size':book_info['score'],
                        'url':book_info['url']
                    }
                )
            return book_list

def getContent():
    contentList = ['Here is a email for you:',
                   'You have a new email for your TomeExchange Account:',
                   'Please click this link to get a new TomeExchange '
                   'Account:',
                   'Welcome to TomeExchange! Click this link to verify your '
                   'account:',
                   'Now, join the best EBook sharing Platform:'
                   ]
    return random.sample(contentList, 1)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/book/<id>')
def book_page(id):
    return render_template('book.html')

@app.route('/map')
def show_map():
    return render_template('map.html')

@app.route('/list')
def book_list():
    return render_template('list.html')


@app.route('/signup')
def signup():
    if session.get('logged_in') is True:
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    if db.register(email, username, password):
        vid = generate_password_hash(email)
        passwd_hash = generate_password_hash(password)
        db.register_temp_user(vid, email, username, passwd_hash)
        content = ('<html>' +
                   getContent()[0] +
                   '<br><a href="http://localhost:4000/verify/' +
                   unicode(vid) +
                   '">click here</a></html>')
        send_mail(EMAIL_ADDRESS_ADMIN, email, EMAIL_SUBJECT_REGISTER, content)
        return 'register success'
    return 'email is used', 400


@app.route('/verify/<vid>')
def verify(vid=None):
    if vid is not None:
        tmp_user = db.get_temp_user(vid)
        if tmp_user is not None:
            if db.query_user(tmp_user['email']) is not None:
                return "User Already Exists"
            else:
                email = tmp_user['email']
                passwd_hash = tmp_user['passwd_hash']
                username = tmp_user['username']

                db.add_user(email, username, passwd_hash)

                db.remove_temp_user(vid)
                session['logged_in'] = True
                session['email'] = email
                return redirect(url_for('home'))
        else:
            abort(404)
    else:
        return abort(404)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if db.login_verify(email, password):
        session['logged_in'] = True
        session['email'] = email
        return 'login success'
    return 'login error', 400


@app.route('/logout', methods=['POST'])
def logout():
    session['logged_in'] = False
    return 'logout success'


@app.route('/download/<string:book_id>')
def download(book_id):
    if session.get('logged_in') is True:
        email = session['email']
        if db.user_ebook_access(email, book_id):
            book = db.book_by_id(book_id)
            dirpath = reduce(os.path.join, [app.root_path, 'static', 'Ebook'])
            storename = book['storename']
            filename = book['filename']
            return send_from_directory(dirpath,
                                       storename,
                                       as_attachment=True,
                                       attachment_filename=filename)
        return abort(404)
    return abort(404)


@app.route('/personal')
def personal():
    if session.get('logged_in') is True:
        return render_template('personal.html')
    else:
        return redirect(url_for('home'))


@app.route('/api/v1/user', methods=['GET', 'POST'])
def users():
    if session.get('logged_in') is True:
        if request.method == 'GET':
            user = db.query_user(session['email'])
            if user:
                return jsonify(user)
            return 'SQL error!', 500
        elif request.method == 'POST':
            username = request.form["name"]
            if db.update_user(session['email'], username):
                return 'update success'
            return 'update error', 500
    return 'not logged in', 400


@app.route('/api/v1/hotbooks', methods=['GET'])
def hot_books():
    num = request.args.get('num')
    books = db.hot_books(int(num))
    return jsonify(books)


@app.route('/api/v1/ebook', methods=['GET'])
def ebook():
    book_id = request.args.get('id')
    book = db.book_by_id(str(book_id))
    return jsonify(book)


@app.route('/api/v1/purchase_verify', methods=['GET'])
def purchase_verify():
    if session.get('logged_in') is True:
        user = db.query_user(session['email'])
        book_id = request.args.get('id')
        book = db.book_by_id(book_id)
        result = jsonify({'current_score': user['score']})
        if (user['score'] >= book['score']):
            return result
        return result, 500
    return 'not logged in', 400


@app.route('/api/v1/purchase', methods=['GET'])
def purchase():
    if session.get('logged_in') is True:
        email = session['email']
        user = db.query_user(email)
        book_id = request.args.get('id')
        book = db.book_by_id(book_id)
        result = jsonify({'current_score': user['score']})
        if (user['score'] >= book['score']):
            db.user_purchase_ebook(email, book_id)
            return result
        return result, 500
    return 'not logged in', 400


@app.route('/api/v1/purchased')
def purchased():
    result = {'purchased': False}
    if session.get('logged_in') is True:
        email = session['email']
        book_id = str(request.args.get('id'))
        if db.user_ebook_access(email, book_id):
            result['purchased'] = True
    return jsonify(result)


@app.route('/api/v1/upload', methods=['POST'])
def upload():
    if session.get('logged_in') is True:
        email = session['email'].encode('utf8')
        name = request.form['name'].encode('utf8')
        author = request.form['author'].encode('utf8')
        category = request.form['catagory'].encode('utf8')
        description = request.form['description'].encode('utf8')
        score = int(request.form['score'])
        file = request.files.get('upload-file')
        image = request.files.get('book-image')
        if file and image:
            file_name = secure_filename(str(datetime.now()) + file.filename)
            file_path = reduce(os.path.join, ['static', 'Ebook', file_name])
            file.save(file_path)
            image_name = secure_filename(str(datetime.now()) + image.filename)
            image_path = reduce(os.path.join, ['static', 'image', image_name])
            image.save(image_path)
            db.upload_ebook(email, name, author, category,
                            description, score, file_name,
                            image_name, file.filename.encode('utf8'))
            return "upload success"
        return "no file uploaded", 300
    return "not logged in", 500


@app.route('/api/v1/upload_list', methods=['GET'])
def update_list():
    if session.get('logged_in') is True:
        email = session['email']
        return jsonify(db.upload_list(email))
    return "not logged in", 500


@app.route('/api/v1/purchase_list', methods=['GET'])
def purchase_list():
    if session.get('logged_in') is True:
        email = session['email']
        return jsonify(db.purchase_list(email))
    return "not logged in", 500


@app.route('/api/v1/subject_map', methods=['GET'])
def subj_map_data():
    json_path = reduce(os.path.join, [app.root_path, 'static', 'data.json'])
    data = json.load(open(json_path))

    cs = db.get_map_book_list('cs')
    print cs
    for c in data['children']:
        if c['name'] == u'工学':
            for cc in c['children']:
                if cc['name'] == u'计算机科学与技术':
                    for ccc in cc['children']:
                        if ccc['name'] == u'计算机软件与理论':
                            ccc.pop('url')
                            ccc.pop('size')
                            ccc['children'] = cs
                            break
                    break
            break

    return jsonify(data)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    db = DataBase()
    app.run(debug=True, host='localhost', port=4000)
