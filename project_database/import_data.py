import pymssql
import json
import copy
import random


class MSSQL:

    def __init__(self,host,user,pwd,db,port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"no dataset informations")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db, charset="utf8",port=self.port)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"connection failed")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

def importDataToFrom(Formname):
    ms = MSSQL(host="192.168.0.109", user="EBook", pwd="ebook", db="ebookdata", port="1434")
    f = open('data.json', 'r')
    hh = json.load(f)
    count = 1

    for field in hh['child']:
        for sec_field in field['child']:
            for paper in sec_field['papers']:
                try:
                    ms.ExecNonQuery("INSERT INTO %s VALUES ('%s', '%s', '%s')"%(Formname, paper['ID'],  field['name'], sec_field['name']))
                except:
                    print 'exception happend ', count, ' times'
                    count += 1
                    continue





def main():
    ms = MSSQL(host="192.168.0.109",user="EBook",pwd="ebook", db="ebookdata", port="1434")
    #ms.ExecNonQuery("INSERT INTO Student_test VALUES ('Gates',  'female', '25')")
    #importDataToFrom('PaperField')
    resList = ms.ExecQuery("SELECT PaperID,Author,Radius FROM PaperAuthorRadius")
    for (paper) in resList:
        print paper
    print len(resList)

if __name__ == '__main__':
    main()