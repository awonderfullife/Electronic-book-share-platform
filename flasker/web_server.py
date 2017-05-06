# -*- coding: utf-8 -*-

from flask import Flask, flash, render_template, request, session
from flask import send_from_directory

from user import User
from config import *


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


@app.route('/login',methods=['GET','POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    user = User(POST_USERNAME)
    result = user.verify_password(POST_PASSWORD)

    if result:
        session['logged_in'] = True
        session['user'] = user.username
    else:
        flash('wrong password!')
    return index()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('welcome.html')
    else:
        return render_template('main.html',user = session.get('user'))



if __name__ == '__main__':
    #ms = MSSQL(host="192.168.0.106",user="EBook",pwd="ebook", db="ebookdata")
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run(host='0.0.0.0', port=1024)
