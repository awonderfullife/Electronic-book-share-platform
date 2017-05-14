import os
import socket

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
basedir = '.'

PORT = 1028
LOCAL_HOST = '192.168.0.103'

DATABASE_HOST = '192.168.0.106'
DATABASE_USER = 'EBook'
DATABASE_PASSWD = 'ebook'
DATABASE_NAME = 'ebookdata'

USER_DATABASE_FILE = 'profiles.json'
VERIFICATION_DATABASE_FILE = 'verify.json'

UPLOAD_FOLDER = os.path.join(os.path.curdir, os.path.sep, 'static', 'Ebook',
                             os.path.sep)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc', 'wps'}
ALLOWED_VERIFY_DURATION = 100

EMAIL_ADDRESS_ADMIN = "sjtu_seiee_se@163.com"
EMAIL_USERNAME = "sjtu_seiee_se"
EMAIL_PASSWORD = "sjtu123"
EMAIL_SENDER = "Admin"

EMAIL_SUBJECT_REGISTER = 'EBook Share Platform Registration'
