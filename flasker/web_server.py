# -*- coding: utf-8 -*-

import time

from flask import Flask, flash, render_template, request, session
from flask import send_from_directory
from werkzeug.security import generate_password_hash

from config import *
from dataBaseSupport import JSONProvider
from emailSupport import send_mail
from user import User, TempUser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

database = JSONProvider()


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


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
