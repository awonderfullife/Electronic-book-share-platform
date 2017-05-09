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
        s = """INSERT INTO UserLogInfo (Mail, PswdHash, NickName) VALUES ('%s', '%s', '%s')""" % (id, password_hash, username)
        self.ExecNonQuery(s)

    def set_password(self, id, username, password_hash):
        s = """INSERT INTO UserLogInfo (Mail, PswdHash, NickName) VALUES ('%s', '%s', '%s')""" % (id, password_hash, username)
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

    def getUserInfo(self, userID):
        if not userID:
            return None
        getuserinfo_sql = """SELECT Mail, NickName, PhoneNum
                                    FROM UserLogInfo
                                    WHERE Mail = '%s' """ % (userID)
        resultList = self.ExecQuery(getuserinfo_sql)
        if len(resultList) != 0:
            userid = resultList[0][0]
            username = resultList[0][1]
            userphone = resultList[0][2]
            userid = userid.rstrip(' ')
            if username is not None:
                username = username.rstrip(' ')
            if userphone is not None:
                userphone.rstrip()
            return [username, userid, userphone]
        return None

    def updateUserInfo(self, userID, userName, phoneNum):
        updateuserinfo_sql = """UPDATE UserLogInfo
                                    SET NickName = '%s', PhoneNum = '%s'
                                    WHERE Mail = '%s' """ % (userName,phoneNum,userID)
        self.ExecNonQuery(updateuserinfo_sql)
        return True

    def filterEbook(self, name="", catagory="", sortby="EBookID", score_low=0,score_high=1000,page=0):
        fliter_sql = ""
        if name != "" and catagory == "":
            fliter_sql = """SELECT EBookID
                            From EBookInfo
                            WHERE Name = '%s' AND Score >= '%d' AND Score <= '%d' AND Page >= '%d'
                            ORDER BY '%s' DESC """ % (name,score_low, score_high, page, sortby)
        if name != "" and catagory != "":
            fliter_sql = """SELECT EBookID
                            From EBookInfo
                            WHERE Name = '%s'AND Type='%s' AND Score >= '%d' AND Score <= '%d' AND Page >= '%d'
                            ORDER BY '%s' DESC """ % (name,catagory, score_low, score_high, page, sortby)
        if name == "" and catagory == "":
            fliter_sql = """SELECT EBookID
                            From EBookInfo
                            WHERE Score >= '%d' AND Score <= '%d' AND Page >= '%d'
                            ORDER BY '%s' DESC """ % (score_low, score_high, page, sortby)
        if name == "" and catagory != "":
            fliter_sql = """SELECT EBookID
                            From EBookInfo
                            WHERE Type='%s' AND Score >= '%d' AND Score <= '%d' AND Page >= '%d'
                            ORDER BY '%s' DESC """ % (catagory, score_low, score_high, page, sortby)
        # print filter_sql
        resultlist = self.ExecQuery(fliter_sql)
        listresult = []
        for item in resultlist:
            listresult.append(item[0])
        # print listresult
        return listresult

    def getEBookInfo(self, EBookID):
        if not EBookID:
            return None
        getbookinfo_sql = """SELECT Name, Type, Notes
                                    FROM EBookInfo
                                    WHERE EBookID = '%s' """ % (EBookID)
        resultList = self.ExecQuery(getbookinfo_sql)
        if len(resultList) != 0:
            bookname = resultList[0][0]
            booktype = resultList[0][1]
            booknotes = resultList[0][2]
            if bookname is not None:
                bookname = bookname.rstrip(' ')
            if booktype is not None:
                booktype = booktype.rstrip(' ')
            if booknotes is not None:
                booknotes.rstrip()
            return [bookname, booktype, booknotes]
        return None

    def updateEBookInfo(self, EBookID, name, type, notes):
        updatebookinfo_sql = """UPDATE EBookInfo
                                    SET Name = '%s', Type = '%s', Notes = '%s'
                                    WHERE EBookID = '%s' """ % (name, type, notes, EBookID)
        self.ExecNonQuery(updatebookinfo_sql)
        return True


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

# ms = SQLProvider()
# print ms.getUserInfo("2441337315@qq.com")
# ms.updateUserInfo("2441337315@qq.com","cooper.yi","15900438037")
# list1 = ms.filterEbook()
# print list1[0]
# print ms.getEBookInfo(list1[0])




