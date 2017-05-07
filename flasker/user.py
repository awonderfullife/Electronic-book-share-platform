from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from dataBaseSupport import SQLProvider


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.database = SQLProvider()
        self.username = self.get_username()
        try:
            self.password_hash = self.get_password_hash().rstrip(' ')
        except AttributeError:
            self.password_hash = None

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """save user name, id and password hash to json file"""
        password_hash = generate_password_hash(password)
        print password_hash
        self.database.set_password(self.id, self.username, password_hash)

    def set_password(self, password):
        password_hash = generate_password_hash(password)
        self.database.set_password(self.id, self.username, password_hash)

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_password_hash(self):
        """try to get password hash from file.

        :return password_hash: if the there is corresponding user in
                the file, return password hash.
                None: if there is no corresponding user, return None.
        """
        return self.database.get_password_hash(self.id)

    def get_username(self):
        return self.database.get_name_by_id(self.id)

    def to_dict(self):
        return {'id': self.id, 'password_hash': self.password_hash,
                'username': self.username}
