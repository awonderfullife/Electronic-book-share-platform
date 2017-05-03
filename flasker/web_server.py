from werkzeug import secure_filename
import os
from flask import Flask, render_template, send_from_directory, request

UPLOAD_FOLDER =os.path.curdir+os.path.sep+'static\Ebook'+os.path.sep
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#@app.route('/database')
#def hello():
#    resList = ms.ExecQuery("SELECT name,sex,class FROM Student_test")
#    return resList[1][1]



if __name__ == '__main__':
    #ms = MSSQL(host="192.168.170.1", user="EBook", pwd="ebook", db="ebookdata")
    app.debug = True
    app.run(host='0.0.0.0', port=1024)