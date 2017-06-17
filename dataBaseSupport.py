# -*- coding: utf-8 -*-
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
                                    charset="UTF-8")
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
        return True

    def removeUser(self, mail):
        if not mail:
            return None
        try:
            delete_sql = """ DELETE FROM UserLogInfo
                                    WHERE Mail = '%s' """ % (mail)
            self.ExecNonQuery(delete_sql)
            return True
        except:
            return False

    def set_password(self, id, password_hash):
        s = """UPDATE UserLogInfo
                    SET PswdHash = '%s'
                    WHERE Mail  = '%s' """ % (password_hash, id)
        self.ExecNonQuery(s)
        return True

    def set_username(self, id, username):
        s = """UPDATE UserLogInfo
                    SET NickName = '%s'
                    WHERE Mail  = '%s' """ % (username, id)
        self.ExecNonQuery(s)
        return True

    def get_password_hash(self, id):
        getpswd_sql = """ SELECT PswdHash
                                FROM UserLogInfo
                                WHERE Mail='%s' """ % (id)
        resultList = self.ExecQuery(getpswd_sql)
        if len(resultList) != 0:
            pswdhash = resultList[0][0]
            if pswdhash is not None:
                pswdhash = pswdhash.rstrip(' ')
            return pswdhash
        return None

    def get_name_by_id(self, user_id):
        if not user_id:
            return None
        getname_sql = """ SELECT NickName
                                FROM UserLogInfo
                                WHERE Mail='%s' """ % (user_id)
        resultList = self.ExecQuery(getname_sql)
        if len(resultList) != 0:
            nickname = resultList[0][0]
            if nickname is not None:
                nickname = nickname.rstrip(' ')
            return nickname
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
                userphone = userphone.rstrip(' ')
            if userid is not None:
                userid = userid.rstrip(' ')
            return [username, userid, userphone, userscore]
        return None

    def updateUserInfo(self, userID, userName, phoneNum):
        updateuserinfo_sql = """UPDATE UserLogInfo
                                    SET NickName = '%s', PhoneNum = '%s'
                                    WHERE Mail = '%s' """ % (userName,phoneNum,userID)
        self.ExecNonQuery(updateuserinfo_sql)
        return True

    def add_ebook(self, id, name, score,rate,download_times,description, author,category,img_url,uploader,created_time,updated_time):
        add_sql_info = """INSERT INTO EBookInfo
                    (EBookID,Name,Type, Notes, Score)
                    VALUES (N'%s', N'%s', N'%s', N'%s', %d)""" % (id, name,
                                                               category, description, score)

        add_sql_basic = """INSERT INTO EBookBasic
                    (EBookID,Name,Type,Note, Score, Rate, DownloadTimes,Author, URL, Uploader, CreateTime, UpdateTime)
                    VALUES (N'%s', N'%s',N'%s',N'%s', %d, %f, %d, N'%s', 
                    N'%s', N'%s',N'%s',N'%s')""" % (id, name,category,
                                                  description, score, rate, download_times, author, img_url, uploader, created_time, updated_time)
        self.ExecNonQuery(add_sql_info)
        self.ExecNonQuery(add_sql_basic)
        return True

    def delete_ebook(self, id):
        try:
            delete_sql_info = """ DELETE FROM EBookInfo
                                    WHERE EBookID = '%s' """ % (id)
            delete_sql_basic = """ DELETE FROM EBookBasic
                                    WHERE EBookID = '%s' """ % (id)
            self.ExecNonQuery(delete_sql_info)
            self.ExecNonQuery(delete_sql_basic)
            return True
        except:
            return False


    def filterEbook(self, name="", catagory="", sortby="EBookID", score_low=0,score_high=1000):
        fliter_sql = ""
        if name != "" and catagory == "":
            fliter_sql = """SELECT EBookID
                            From EBookInfo
                            WHERE Name = '%s' AND Score >= '%d' AND Score <= '%d'
                            ORDER BY '%s' DESC """ % (name,score_low, score_high, sortby)
        if name != "" and catagory != "":
            fliter_sql = """SELECT EBookID
                            From EBookInfo
                            WHERE Name = '%s'AND Type='%s' AND Score >= '%d' AND Score <= '%d'
                            ORDER BY '%s' DESC """ % (name,catagory, score_low, score_high, sortby)
        if name == "" and catagory == "":
            fliter_sql = """SELECT EBookID
                            From EBookInfo
                            WHERE Score >= '%d' AND Score <= '%d'
                            ORDER BY '%s' DESC """ % (score_low, score_high, sortby)
        if name == "" and catagory != "":
            fliter_sql = """SELECT EBookID
                            From EBookInfo
                            WHERE Type='%s' AND Score >= '%d' AND Score <= '%d'
                            ORDER BY '%s' DESC """ % (catagory, score_low, score_high, sortby)
        # print filter_sql
        resultlist = self.ExecQuery(fliter_sql)
        listresult = []
        for item in resultlist:
            mes = item[0]
            if mes is not None:
                mes = mes.rstrip(' ')
            listresult.append(mes)
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


    def add_user_purchased_EBook(self, user_id, book_id):
        add_sql = """INSERT INTO UserPurchased
                    (Mail, EBookID)
                    VALUES ('%s', '%s')""" % (user_id, book_id)
        self.ExecNonQuery(add_sql)
        return True

    def check_user_purchased_EBook(self, user_id, book_id):
        seek_sql = """SELECT Mail, EBookID
                                    FROM UserPurchased
                                    WHERE Mail = '%s' AND EBookID = '%s' """ % (user_id, book_id)
        result_list = self.ExecQuery(seek_sql)
        if len(result_list) != 0:
            return True
        else:
            return False

    def delete_user_purchased_EBook(self, user_id, book_id):
        try:
            delete_sql = """ DELETE FROM UserPurchased
                                    WHERE Mail = '%s' AND EBookID = '%s' """ % (user_id, book_id)
            self.ExecNonQuery(delete_sql)
            return True
        except:
            return False

    def delete_user_purchased_ebookid(self,book_id):
        try:
            delete_sql = """ DELETE FROM UserPurchased
                                    WHERE EBookID = '%s' """ % (book_id)
            self.ExecNonQuery(delete_sql)
            return True
        except:
            return False


    def get_user_purchased_EBook_list(self, user_id):
        if not user_id:
            return None
        getinfo_sql = """SELECT EBookID
                                    FROM UserPurchased
                                    WHERE Mail = '%s' """ % (user_id)
        resultList = self.ExecQuery(getinfo_sql)
        listresult = []
        for item in resultList:
            mes = item[0]
            if mes is not None:
                mes = mes.rstrip(' ')
            listresult.append(mes)
        return listresult

    def add_user_favored_EBook(self, user_id, book_id):
        add_sql = """INSERT INTO UserFavored
                    (Mail, EBookID)
                    VALUES ('%s', '%s')""" % (user_id, book_id)
        self.ExecNonQuery(add_sql)
        return True

    def check_user_favored_EBook(self, user_id, book_id):
        seek_sql = """SELECT Mail, EBookID
                                    FROM UserFavored
                                    WHERE Mail = '%s' AND EBookID = '%s' """ % (user_id, book_id)
        result_list = self.ExecQuery(seek_sql)
        if len(result_list) != 0:
            return True
        else:
            return False

    def delete_user_favored_EBook(self, user_id, book_id):
        try:
            delete_sql = """ DELETE FROM UserFavored
                                    WHERE Mail = '%s' AND EBookID = '%s' """ % (user_id, book_id)
            self.ExecNonQuery(delete_sql)
            return True
        except:
            return False

    def delete_user_favored_ebookid(self,book_id):
        try:
            delete_sql = """ DELETE FROM UserFavored
                                    WHERE EBookID = '%s' """ % (book_id)
            self.ExecNonQuery(delete_sql)
            return True
        except:
            return False

    def get_user_favored_EBook_list(self, user_id):
        if not user_id:
            return None
        getinfo_sql = """SELECT EBookID
                                    FROM UserFavored
                                    WHERE Mail = '%s' """ % (user_id)
        resultList = self.ExecQuery(getinfo_sql)
        listresult = []
        for item in resultList:
            mes = item[0]
            if mes is not None:
                mes = mes.rstrip(' ')
            listresult.append(mes)
        return listresult



    def add_user_uploaded_EBook(self, user_id, book_id):
        add_sql = """INSERT INTO UserUploaded
                    (Mail, EBookID)
                    VALUES (N'%s', N'%s')""" % (user_id, book_id)
        self.ExecNonQuery(add_sql)
        return True

    def check_user_uploaded_EBook(self, user_id, book_id):
        seek_sql = """SELECT Mail, EBookID
                                    FROM UserUploaded
                                    WHERE Mail = '%s' AND EBookID = '%s' """ % (user_id, book_id)
        result_list = self.ExecQuery(seek_sql)
        if len(result_list) != 0:
            return True
        else:
            return False

    def delete_user_uploaded_EBook(self, user_id, book_id):
        try:
            delete_sql = """ DELETE FROM UserUploaded
                                    WHERE Mail = '%s' AND EBookID = '%s' """ % (user_id, book_id)
            self.ExecNonQuery(delete_sql)
            return True
        except:
            return False

    def delete_user_uploaded_ebookid(self,book_id):
        try:
            delete_sql = """ DELETE FROM UserUploaded
                                    WHERE EBookID = '%s' """ % (book_id)
            self.ExecNonQuery(delete_sql)
            return True
        except:
            return False

    def get_user_uploaded_EBook_list(self, user_id):
        if not user_id:
            return None
        getinfo_sql = """SELECT EBookID
                                    FROM UserUploaded
                                    WHERE Mail = '%s' """ % (user_id)
        resultList = self.ExecQuery(getinfo_sql)
        listresult = []
        for item in resultList:
            mes = item[0]
            if mes is not None:
                mes = mes.rstrip(' ')
            listresult.append(mes)
        return listresult

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

    def add_EBook_FileStoredName(self, EBookID, filename, storedname):
        s = """INSERT INTO EBookFile
                    (EBookID, FileName, StoreName)
                    VALUES (N'%s', N'%s', N'%s')""" % (EBookID, filename,
                                                     storedname)
        self.ExecNonQuery(s)
        return True

    def delete_EBook_FileStoredName(self,EBookID):
        if not EBookID:
            return None
        try:
            delete_sql = """ DELETE FROM EBookFile
                                    WHERE EBookID = '%s' """ % (EBookID)
            self.ExecNonQuery(delete_sql)
            return True
        except:
            return False

    def get_EBook_FileStoredName(self, EBookID):
        seek_sql = """SELECT FileName, StoreName
                                FROM EBookFile
                                WHERE EBookID = '%s' """ % (EBookID)
        result_list = self.ExecQuery(seek_sql)
        if len(result_list) != 0:
            filename = result_list[0][0]
            storename = result_list[0][1]
            if filename is not None:
                filename = filename.rstrip(' ')
            if storename is not None:
                storename = storename.rstrip(' ')
            return [filename, storename]
        else: return []




    def add_temp_user(self,vid,info_list):
        s = """INSERT INTO TempUser
                    (Vid, Mail, NickName, PswdHash, RegisterTime)
                    VALUES ('%s', '%s', '%s', '%s', %d)""" % (vid, info_list[0], info_list[1], info_list[2], info_list[3])
        self.ExecNonQuery(s)
        return True

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
