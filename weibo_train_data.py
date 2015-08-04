__author__ = 'Des'

import mysql.connector
from mysql.connector import errorcode

from sql_config import *

__metaclass__ = type


class WeiboTrainData:
    def __init__(self):
        self.table_name = 'weibo_train_data'
        self.array_size = 100000
        try:
            self.cnx = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.cnx.cursor()
            self.cnx.database = DB_NAME
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Username or password is wrong")
            else:
                print(err.msg)

    def __enter__(self):
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.cursor.close()
            self.cnx.close()
        except mysql.connector.Error as err:
            print(err.msg)

    def exe(self, ddl):
        try:
            self.cursor.execute(ddl)
        except mysql.connector.Error as err:
            print(err.msg)
        return self.cursor.fetchall()

    def exe_many(self, ddl, seq):
        try:
            self.cursor.executemany(ddl, seq)
        except mysql.connector.Error as err:
            print(err.msg)
        return self.cursor.fetchall()

    def get_all_uid(self):
        self.cursor.execute("SELECT DISTINCT uid FROM " + self.table_name)
        return self.cursor.fetchall()

    def gen_all_uid(self):
        self.cursor.execute("SELECT DISTINCT uid FROM " + self.table_name)
        results = self.cursor.fetchall()
        if results:
            for r in results:
                yield r

    def gen_all(self):
        self.cursor.execute("SELECT * FROM " + self.table_name)
        results = self.cursor.fetchall()
        if results:
            for r in results:
                yield r

    def get_by_uid(self, con):
        self.cursor.execute("SELECT * FROM " + self.table_name + " WHERE uid={}".format(con))
        return self.cursor.fetchall()

    def get_by_time(self, con):
        self.cursor.execute("SELECT * FROM " + self.table_name + " WHERE time={}".format(con))
        return self.cursor.fetchall()

    def get_between_time(self, con1, con2):
        self.cursor.execute("SELECT * FROM " + self.table_name + " WHERE time BETWEEN '{}' AND '{}'".format(con1, con2))
        return self.cursor.fetchall()
