# -*- coding: utf-8 -*-
import json
import pymssql
from config import *
import json
import pymssql

from config import *


class SQLProvider:
    def __init__(self):
        self.host = DATABASE_HOST
        self.user = DATABASE_USER
        self.pwd = DATABASE_PASSWD
        self.db = DATABASE_NAME

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "no dataset informations")
        self.conn = pymssql.connect(host=self.host, user=self.user,
                                    password=self.pwd, database=self.db,
                                    charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "connection failed")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def add_user(self, id, username, password_hash):
        s = """INSERT INTO UserLogInfo VALUES ('%s', '%s', '%s')""" % (id, password_hash, username)
        self.ExecNonQuery(s)

    def set_password(self, id, username, password_hash):
        s = """INSERT INTO UserLogInfo VALUES ('%s', '%s', '%s')""" % (id, password_hash, username)
        self.ExecNonQuery(s)

    def get_password_hash(self, id):
        getpswd_sql = """ SELECT PswdHash FROM UserLogInfo WHERE Mail='%s' """ % (id)
        resultList = self.ExecQuery(getpswd_sql)
        if len(resultList) != 0:
            return resultList[0][0]
        return None

    def get_name_by_id(self, user_id):
        if not user_id:
            return None
        getname_sql = """ SELECT NickName FROM UserLogInfo WHERE Mail='%s' """ % (user_id)
        resultList = self.ExecQuery(getname_sql)
        if len(resultList) != 0:
            return resultList[0][0]
        return None


class JSONProvider:
    def __init__(self):
        self.user_database_file = USER_DATABASE_FILE
        self.verification_database_file = VERIFICATION_DATABASE_FILE

    def add_user(self, id, username, password_hash):
        with open(self.user_database_file, 'r+') as f:
            profiles = json.load(f)
            profiles[id] = [password_hash, username]

            with open(self.user_database_file, 'w+') as newF:
                newF.write(json.dumps(profiles))

    def set_password(self, id, username, password_hash):
        with open(self.user_database_file, 'r+') as f:

            profiles = json.load(f)
            profiles[id] = [password_hash, username]

            with open(self.user_database_file, 'w+') as newF:
                newF.write(json.dumps(profiles))

    def get_password_hash(self, id):
        try:
            with open(self.user_database_file) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(id, None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_name_by_id(self, user_id):
        if not user_id:
            return None
        try:
            with open(self.user_database_file) as f:
                user_profiles = json.load(f)
                if user_id in user_profiles:
                    return user_profiles[user_id][1]

        except:
            return None
        return None

    def add_temp_user(self,vid,info_list):
        with open(self.verification_database_file, 'r+') as f:
            profiles = json.load(f)
            profiles[vid] = info_list

            with open(self.verification_database_file, 'w+') as newF:
                newF.write(json.dumps(profiles))

    def get_temp_user(self,vid):
        if not vid:
            return None
        try:
            with open(self.verification_database_file) as f:
                user_profiles = json.load(f)
                if vid in user_profiles:
                    return user_profiles[vid]

        except:
            return None
        return None

    def validate_temp_user(self,vid):
        if not vid:
            return None
        try:
            with open(self.verification_database_file) as f:
                user_profiles = json.load(f)
                user_profiles.pop(vid,None)
                with open(self.verification_database_file, 'w+') as newF:
                    newF.write(json.dumps(user_profiles))
        except:
            return None
        return None
