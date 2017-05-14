# -*- coding: utf-8 -*-
import json
import pymssql
from config import *
import json
import pymssql

from config import *

"""
Attention: Don't change any char in this file to avoid unnecessary conflicts
just contact with cooper.yi ~
Created by : Cooper yi
Date : 2017/5/9
"""


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
        s = """INSERT INTO UserLogInfo
                    (Mail, PswdHash, NickName)
                    VALUES ('%s', '%s', '%s')""" % (id, password_hash, username)
        self.ExecNonQuery(s)

    def set_password(self, id, username, password_hash):
        s = """INSERT INTO UserLogInfo
                    (Mail, PswdHash, NickName)
                    VALUES ('%s', '%s', '%s')""" % (id, password_hash, username)
        self.ExecNonQuery(s)

    def get_password_hash(self, id):
        getpswd_sql = """ SELECT PswdHash
                                FROM UserLogInfo
                                WHERE Mail='%s' """ % (id)
        resultList = self.ExecQuery(getpswd_sql)
        if len(resultList) != 0:
            return resultList[0][0]
        return None

    def get_name_by_id(self, user_id):
        if not user_id:
            return None
        getname_sql = """ SELECT NickName
                                FROM UserLogInfo
                                WHERE Mail='%s' """ % (user_id)
        resultList = self.ExecQuery(getname_sql)
        if len(resultList) != 0:
            return resultList[0][0]
        return None

    def getUserInfo(self, userID):
        if not userID:
            return None
        getuserinfo_sql = """SELECT Mail, NickName, PhoneNum, Score
                                    FROM UserLogInfo
                                    WHERE Mail = '%s' """ % (userID)
        resultList = self.ExecQuery(getuserinfo_sql)
        if len(resultList) != 0:
            userid = resultList[0][0]
            username = resultList[0][1]
            userphone = resultList[0][2]
            userscore = resultList[0][3]
            userid = userid.rstrip(' ')
            if username is not None:
                username = username.rstrip(' ')
            if userphone is not None:
                userphone.rstrip()
            return [username, userid, userphone, userscore]
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
        getbookinfo_sql = """SELECT Name, Type, Note, Score, Rate, DownLoadTimes, Author, URL, Uploader, CreateTime, UpdateTime
                                    FROM EBookBasic
                                    WHERE EBookID = '%s' """ % (EBookID)
        resultList = self.ExecQuery(getbookinfo_sql)
        if len(resultList) != 0:
            bookname = resultList[0][0]
            booktype = resultList[0][1]
            booknotes = resultList[0][2]
            score = resultList[0][3]
            rate = resultList[0][4]
            download_times = resultList[0][5]
            author = resultList[0][6]
            img_url = resultList[0][7]
            uploader = resultList[0][8]
            create_at = resultList[0][9]
            updates_at = resultList[0][10]

            if bookname is not None:
                bookname = bookname.rstrip(' ')
            if booktype is not None:
                booktype = booktype.rstrip(' ')
            if booknotes is not None:
                booknotes = booknotes.rstrip(' ')
            if author is not None:
                author = author.rstrip(' ')
            if img_url is not None:
                img_url = img_url.rstrip(' ')
            if uploader is not None:
                uploader = uploader.rstrip(' ')
            if create_at is not None:
                create_at = create_at.rstrip(' ')
            if updates_at is not None:
                updates_at = updates_at.rstrip(' ')

            return [bookname, booktype, booknotes, score, rate, download_times, author, img_url, uploader, create_at, updates_at]
        return None

    def getEBookInfo2(self, EBookID):
        if not EBookID:
            return None
        getbookinfo_sql = """SELECT Name, Score, EBookID, URL, Uploader, CreateTime, UpdateTime
                                    FROM EBookBasic
                                    WHERE EBookID = '%s' """ % (EBookID)
        resultList = self.ExecQuery(getbookinfo_sql)
        if len(resultList) != 0:
            bookname = resultList[0][0]
            score = resultList[0][1]
            bookid = resultList[0][2]
            img_url = resultList[0][3]
            uploader = resultList[0][4]
            create_at = resultList[0][5]
            updates_at = resultList[0][6]

            bookid = bookid.rstrip(' ')
            if bookname is not None:
                bookname = bookname.rstrip(' ')
            if img_url is not None:
                img_url = img_url.rstrip(' ')
            if uploader is not None:
                uploader = uploader.rstrip(' ')
            if create_at is not None:
                create_at = create_at.rstrip(' ')
            if updates_at is not None:
                updates_at = updates_at.rstrip(' ')

            return [bookname, score, bookid, img_url, uploader, create_at, updates_at]
        return None

    def updateEBookInfo(self, EBookID, name, type, score):
        updatebookinfo_sql = """UPDATE EBookInfo
                                    SET Name = '%s', Type = '%s', Score = '%s'
                                    WHERE EBookID = '%s' """ % (name, type, score, EBookID)
        self.ExecNonQuery(updatebookinfo_sql)
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET Name = '%s', Type = '%s', Score = '%s'
                                    WHERE EBookID = '%s' """ % (name, type, score, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyUserScore(self, Mail, newScore):
        updatebookinfo_sql = """UPDATE UserLogInfo
                                    SET Score = %d
                                    WHERE Mail = '%s' """ % (newScore, Mail)
        self.ExecNonQuery(updatebookinfo_sql)
        return True

    def modifyEBookName(self, EBookID, newName):
        updatebookinfo_sql = """UPDATE EBookInfo
                                    SET Name = '%s'
                                    WHERE EBookID = '%s' """ % (newName, EBookID)
        self.ExecNonQuery(updatebookinfo_sql)
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET Name = '%s'
                                    WHERE EBookID = '%s' """ % (newName, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookType(self, EBookID, newType):
        updatebookinfo_sql = """UPDATE EBookInfo
                                    SET Type = '%s'
                                    WHERE EBookID = '%s' """ % (newType, EBookID)
        self.ExecNonQuery(updatebookinfo_sql)
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET Type = '%s'
                                    WHERE EBookID = '%s' """ % (newType, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookNotes(self, EBookID, newNotes):
        updatebookinfo_sql = """UPDATE EBookInfo
                                    SET Notes = '%s'
                                    WHERE EBookID = '%s' """ % (newNotes, EBookID)
        self.ExecNonQuery(updatebookinfo_sql)
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET Note = '%s'
                                    WHERE EBookID = '%s' """ % (newNotes, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookScore(self, EBookID, newScore):
        updatebookinfo_sql = """UPDATE EBookInfo
                                    SET Score = %d
                                    WHERE EBookID = '%s' """ % (newScore, EBookID)
        self.ExecNonQuery(updatebookinfo_sql)
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET Score = %d
                                    WHERE EBookID = '%s' """ % (newScore, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookRate(self, EBookID, newRate):
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET Rate = %f
                                    WHERE EBookID = '%s' """ % (newRate, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookDlTimes(self, EBookID, newTimes):
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET DownloadTimes = %d
                                    WHERE EBookID = '%s' """ % (newTimes, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookAuthor(self, EBookID, newAuthor):
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET Author = '%s'
                                    WHERE EBookID = '%s' """ % (newAuthor, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookURL(self, EBookID, newURL):
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET URL = '%s'
                                    WHERE EBookID = '%s' """ % (newURL, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookUploader(self, EBookID, newUploader):
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET Uploader = '%s'
                                    WHERE EBookID = '%s' """ % (newUploader, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookCreateTime(self, EBookID, newCreateTime):
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET CreateTime = '%s'
                                    WHERE EBookID = '%s' """ % (newCreateTime, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def modifyEBookUpdateTime(self, EBookID, newUpdateTime):
        updatebookinfo_sql2 = """UPDATE EBookBasic
                                    SET UpdateTime = '%s'
                                    WHERE EBookID = '%s' """ % (newUpdateTime, EBookID)
        self.ExecNonQuery(updatebookinfo_sql2)
        return True

    def addUserRBook(self, Mail, EBookID):
        add_sql = """INSERT INTO MailEBook
                    (Mail, EBookID)
                    VALUES ('%s', '%s')""" % (Mail, EBookID)
        self.ExecNonQuery(add_sql)

    def checkUserEBook(self, Mail, EBookID):
        seek_sql = """SELECT Mail, EBookID
                                    FROM MailEBook
                                    WHERE Mail = '%s' AND EBookID = '%s' """ % (Mail, EBookID)
        result_list = self.ExecQuery(seek_sql)
        if len(result_list) != 0:
            return True
        else:
            return False

    def getEBookFileName(self, EBookID):
        seek_sql = """SELECT FileName
                                FROM EBookFile
                                WHERE EBookID = '%s' """ % (EBookID)
        result_list = self.ExecQuery(seek_sql)
        if len(result_list) != 0:
            return result_list[0][0]
        else: return None

    def testFunction(self):
        if True:
            return None
        test_sql = """SELECT EBookID
                        From EBookInfo"""
        result1 = self.ExecQuery(test_sql)
        test_sql2 = """SELECT EBookID
                    From EBookBasic"""
        result2 = self.ExecQuery(test_sql2)
        index1 = 0
        index2 = 0
        count = 0
        while(index1 < len(result1) and index2 < len(result2)):
            if (result1[index1][0] > result2[index2][0]): index2 += 1
            elif (result1[index1][0] == result2[index2][0]):
                index2 +=1
                index1 +=1
            else:
                index1 += 1
                count += 1
        print len(result1), len(result2)
        print index1, index2, count

    def inserDataFunction(self):
        if True:
            return None
        seek_sql = """SELECT EBookID
                                FROM EBookInfo"""
        result_list = self.ExecQuery(seek_sql)
        for item in result_list:
            try:
                insert_sql = """INSERT INTO EBookFile
                            (EBookID, FileName)
                            VALUES ('%s', 'FFFFFFFF.pdf')""" % (item[0])
                self.ExecNonQuery(insert_sql)
            except:
                print 'oh no!'

    def add_temp_user(self,vid,info_list):
        s = """INSERT INTO TempUser
                    (Vid, Mail, NickName, PswdHash, RegisterTime)
                    VALUES ('%s', '%s', '%s', '%s', %d)""" % (vid, info_list[0], info_list[1], info_list[2], info_list[3])
        self.ExecNonQuery(s)

    def get_temp_user(self,vid):
        if not vid:
            return None
        getinfo_sql = """SELECT Mail, NickName, PswdHash, RegisterTime
                                    FROM TempUser
                                    WHERE Vid = '%s' """ % (vid)
        resultList = self.ExecQuery(getinfo_sql)
        if len(resultList) != 0:
            mail = resultList[0][0]
            username = resultList[0][1]
            pswdhash = resultList[0][2]
            registertime = resultList[0][3]
            if mail is not None:
                mail = mail.rstrip(' ')
            if username is not None:
                username = username.rstrip(' ')
            if pswdhash is not None:
                pswdhash = pswdhash.rstrip(' ')
            return [mail, username, pswdhash, registertime]
        else:
            return None

    def validate_temp_user(self,vid):
        if not vid:
            return None
        try:
            delete_sql = """ DELETE FROM TempUser
                                    WHERE Vid = '%s' """ % (vid)
            self.ExecNonQuery(delete_sql)
        except:
            return None







class JSONProvider:
    def __init__(self):
        self.user_database_file = USER_DATABASE_FILE
        self.verification_database_file = VERIFICATION_DATABASE_FILE

    # finished
    def add_user(self, id, username, password_hash):
        with open(self.user_database_file, 'r+') as f:
            profiles = json.load(f)
            profiles[id] = [password_hash, username]

            with open(self.user_database_file, 'w+') as newF:
                newF.write(json.dumps(profiles))

    # finished
    def set_password(self, id, username, password_hash):
        with open(self.user_database_file, 'r+') as f:

            profiles = json.load(f)
            profiles[id] = [password_hash, username]

            with open(self.user_database_file, 'w+') as newF:
                newF.write(json.dumps(profiles))

    # finished
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

    # finished
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

"""
blow is the code that success run in my computer, and it does modify or
feached the data we needed.
"""
#ms = SQLProvider()
#print ms.getUserInfo("2441337315@qq.com")
#ms.updateUserInfo("2441337315@qq.com","cooper.yi","15900438037")
#list1 = ms.filterEbook()
#print list1[0]
#print ms.getEBookInfo(list1[0])
#ms.updateEBookInfo('002D06F3', 'goodstory', 'Computer Science', 999)
#print ms.getEBookInfo('002D06F3')
#print ms.getEBookInfo2('002D06F3')
#ms.modifyEBookName('002D06F3', 'awonderfullife')
#ms.modifyEBookType('002D06F3','Person Stroy')
#ms.modifyEBookNotes('002D06F3', 'a interesting stroy about cooper')
#ms.modifyEBookScore('002D06F3', 10)
#ms.modifyEBookRate('002D06F3', 99.9)
#ms.modifyEBookDlTimes('002D06F3', 24)
#ms.modifyEBookAuthor('002D06F3', 'Cooper_YI')
#ms.modifyEBookURL('002D06F3','www.google.com')
#ms.modifyEBookUploader('002D06F3','cooper.yyq')
#ms.modifyEBookCreateTime('002D06F3','2017-6-6 18:02:45')
#ms.modifyEBookUpdateTime('002D06F3', '2017-7-7 12:03:12')
#ms.modifyUserScore('223',18)
#ms.addUserRBook('223','002D06F3')
#print ms.checkUserEBook('223','002D06F3')
#print ms.checkUserEBook('224','002D06F3')
#print ms.checkUserEBook('223','002D06F4')
#print ms.getEBookFileName('002D06F3')
#ms.add_temp_user('123456',['c@qq.com', 'cooper', 'HHHH', 123])
#print ms.get_temp_user('123456')
#ms.validate_temp_user('123456')

