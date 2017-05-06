import imp

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import json
import uuid
from dataBaseSupport import JSONProvider


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.database = JSONProvider()
        self.password_hash = self.get_password_hash()
        self.id = self.get_id()
  # SQL

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """save user name, id and password hash to json file"""
        password_hash = generate_password_hash(password)
        self.database.set_password(self.username, password_hash, self.id)

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
        return self.database.get_password_hash(username=self.username)

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        return self.database.get_id(self.username)

    def get(self, user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        username = self.database.get_name_by_id(user_id)
        if username is None:
            return None
        else:
            return User(username)
