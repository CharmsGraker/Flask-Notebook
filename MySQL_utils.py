import pymysql
import traceback
import sys

class MysqlUtils:
    def __init__(self):
        host = '127.0.0.1'
        user = 'root'
        password = 'root'
        database = 'notebook_database'
        self.db = pymysql.connect(host=host, user=user, password=password, db=database)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor) # 将游标设置为字典型

    def insert(self, sql):
        '''
        插入项

        :param sql:为SQL里的执行语句
        :return:
        '''
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            print("插入表项发生异常")
            self.db.rollback()
        finally:
            self.db.close()

    def fetchone(self, sql):
        '''
        查询数据库
        '''
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except:
            traceback.print_exc()
            self.db.rollback()
        finally:
            self.db.close()
        return result

    def fetchall(self, sql):
        '''
        查询所有记录，用于查询试图登录的用户信息
        :param sql:
        :return:
        '''
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            info = sys.exc_info()
            print(info[0],':', info[1])
        self.db.rollback()
        return results

    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            f = open("\log.txt",'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            self.db.rollback()
        finally:
            self.db.close()

    def update(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            self.db.close()
