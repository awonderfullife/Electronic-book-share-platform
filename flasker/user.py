# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from config import *
from dataBaseSupport import SQLProvider, JSONProvider


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.database = JSONProvider()
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

    def set_info(self):
        self.database.set_password(self.id, self.username, self.password_hash)

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


class TempUser:
    def __init__(self, vid):
        self.vid = vid
        self.database = JSONProvider()
        self.existence = False
        self.user_info = self.database.get_temp_user(self.vid)

    def validate_time(self, time):
        if self.vid is None:
            raise KeyError
        else:
            if self.user_info is None:
                raise KeyError
            if int(time) - int(self.user_info[3]) < ALLOWED_VERIFY_DURATION:
                return True
            else:
                return False


    # Get information of this temp user
    def get_info(self):
        pass

    def set_password(self,passwd):
        try:
            self.user_info[2] = generate_password_hash(passwd)
        except IndexError:
            self.user_info.append( generate_password_hash(passwd))

    def add_user(self):
        self.database.add_temp_user(self.vid,self.user_info)

    def check_user_existence(self):
        return self.database.get_name_by_id(self.user_info[0])

    def to_real_user(self):
        new_u = User(self.user_info[0])
        new_u.username = self.user_info[1]
        new_u.password_hash = self.user_info[2]
        new_u.set_info()
        self.database.validate_temp_user(self.vid)
        return new_u
