import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
basedir = '.'

UPLOAD_FOLDER =os.path.curdir+os.path.sep+'static\Ebook'+os.path.sep
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc', 'wps'}

EMAIL_ADDRESS = "sjtu_seiee_se@163.com"
EMAIL_USERNAME = "sjtu_seiee_se"
EMAIL_PASSWORD = "sjtu123"
