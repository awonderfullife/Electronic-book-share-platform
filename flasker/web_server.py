# -*- coding: utf-8 -*-

from flask import Flask, flash, render_template, request, session
from flask import send_from_directory
from werkzeug.security import generate_password_hash

from config import *
from emailSupport import send_to_mail
from user import User

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    post_id = str(request.form['id'])
    post_password = str(request.form['password'])

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
    post_id = str(request.form['id'])
    post_password = str(request.form['password'])
    post_username = str(request.form['username'])

    user = User(post_id)
    if user.username is None:
        vid = generate_password_hash(post_id)
        session[vid] = user.to_dict()
        session[vid]['password'] = post_password
        session[vid]['username'] = post_username
        url = "localhost:1024/verify/" + str(vid)
        send_to_mail(post_id, url)
        return render_template('success.html')


@app.route('/verify/<vid>')
def verify(vid=None):
    if vid is not None and session.get(vid) is not None:
        try:
            user_dict = dict(session.get(vid))
            print user_dict
            new_user = User(user_dict['id'])
            new_user.username = user_dict['username']
            new_user.set_password(user_dict['password'])
            session['logged_in'] = True
            session['user'] = new_user.to_dict()
            return render_template('register_complete.html', username=
            user_dict['username'])
        except KeyError:
            pass


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
    # ms = MSSQL(host="192.168.0.106",user="EBook",pwd="ebook", db="ebookdata")

    app.secret_key = os.urandom(12)
    app.debug = True
    app.run(host='0.0.0.0', port=1024)
