import imp
import json
import pymssql

SQL = imp.load_source('MSSQL', '../project_database/sql_operate.py')
databaseName = "ebookdata"
# databaseName = "UserLogInfo"
ms = SQL.MSSQL(host="192.168.0.106", user="EBook", pwd="ebook",
               db=databaseName)


class SQLProvider:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

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


class JSONProvider:
    def __init__(self):
        self.database_file = "profiles.json"

    def add_user(self, id, username, password_hash):
        with open(self.database_file, 'r+') as f:
            profiles = json.load(f)
            profiles[id] = [password_hash, username]

            with open(self.database_file, 'w+') as newF:
                newF.write(json.dumps(profiles))

    def set_password(self, id, username, password_hash):
        with open(self.database_file, 'r+') as f:

            profiles = json.load(f)
            profiles[id] = [password_hash, username]

            with open(self.database_file, 'w+') as newF:
                newF.write(json.dumps(profiles))

    def get_password_hash(self, id):
        try:
            with open(self.database_file) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(id, None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    # def get_id(self, username):
    #     if username is not None:
    #         try:
    #             with open(self.database_file) as f:
    #                 user_profiles = json.load(f)
    #                 if username in user_profiles:
    #                     return user_profiles[username][1]
    #         except IOError:
    #             pass
    #         except ValueError:
    #             pass
    #     return unicode(uuid.uuid4())

    def get_name_by_id(self, user_id):
        if not user_id:
            return None
        try:
            with open(self.database_file) as f:
                user_profiles = json.load(f)
                if user_id in user_profiles:
                    return user_profiles[user_id][1]

        except:
            return None
        return None
