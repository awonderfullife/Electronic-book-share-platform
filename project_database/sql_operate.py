import pymssql


class MSSQL:

    data = [['hz567','tang','123'],['hz678','song','234'],['hz789','kai',
                                                           '345']]

    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"no dataset informations")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"connection failed")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        try:
            resList = cur.fetchall()
            self.conn.close()
            return resList

        except pymssql.OperationalError:
            return None


    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def addUser(self,id,nickName):
        # query = "INSERT INTO UserLogInfo (UserID, nickName, passWord) VALUES(" \
        #         + str(id)+","+  str(nickName)  +",'huzong666');"
        # self.ExecNonQuery(query)
        for u in self.data:
            if u[0] == id:
                return
        self.data.append([id,nickName,'233'])


def main():
    databaseName = "ebookdata"
    # databaseName = "UserLogInfo"
    ms = MSSQL(host="192.168.0.106",user="EBook",pwd="ebook", db=databaseName)
    # query = "SELECT name,sex,class FROM Student_test"
    # query = "SELECT UserID, nickName, passWord FROM UserLogInfo "
    query = "INSERT INTO UserLogInfo (UserID, nickName, passWord) VALUES(" \
            "'53E34','HU ZONG','huzong666');"

    resList = ms.ExecNonQuery(query)

    query = "SELECT UserID, nickName, passWord FROM UserLogInfo "
    resList = ms.ExecQuery(query)
    if resList is not None:
        for student in resList:
            print student

if __name__ == '__main__':
    main()