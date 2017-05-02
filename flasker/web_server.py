from flask import Flask
from flask import request
from flask import render_template
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER =os.path.curdir+os.path.sep+'Ebook'+os.path.sep
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html')
    return render_template('upload.html')




#@app.route('/database')
#def hello():
#    resList = ms.ExecQuery("SELECT name,sex,class FROM Student_test")
#    return resList[1][1]


if __name__ == '__main__':
    #ms = MSSQL(host="192.168.170.1", user="EBook", pwd="ebook", db="ebookdata")
    app.debug = True
    app.run(host='0.0.0.0', port=1024)