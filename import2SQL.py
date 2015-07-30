__author__ = 'Desmond'

import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost'
}

DB_NAME = "tianchi_weibo"

table1 = "weibo_train_data"
TABLES = {}
TABLES[table1] = (
    "CREATE TABLE IF NOT EXISTS `" + table1 + "` ("
                                              "`uid` char(32) NOT NULL,"
                                              "`mid` char(32) NOT NULL,"
                                              "`time` date NOT NULL,"
                                              "`forward_count` int NOT NULL,"
                                              "`comment_count` int NOT NULL,"
                                              "`like_count` int NOT NULL,"
                                              "`content` text NOT NULL"
                                              ") ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;"
)

add_table1 = ("INSERT INTO  " + table1 +
              "(uid, mid, time, forward_count, comment_count, like_count, content) "
              "VALUES (%s, %s, %s, %s, %s, %s, %s)")

table2 = "weibo_predict_data"
TABLES[table2] = (
    "CREATE TABLE IF NOT EXISTS `" + table2 + "` ("
                                              "`uid` char(32) NOT NULL,"
                                              "`mid` char(32) NOT NULL,"
                                              "`time` date NOT NULL,"
                                              "`content` text NOT NULL"
                                              ") ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;"
)

add_table2 = ("INSERT INTO " + table2 +
              "(uid, mid, time, content) "
              "VALUES (%s, %s, %s, %s)")

CREATE_INDEXS = [
    "ALTER TABLE `" + table1 + "` ADD INDEX(`uid`);",
    "ALTER TABLE `" + table1 + "` ADD INDEX(`mid`);",
    "ALTER TABLE `" + table2 + "` ADD INDEX(`uid`);",
    "ALTER TABLE `" + table2 + "` ADD INDEX(`mid`);"]

try:
    cnx = mysql.connector.connect(**DB_CONFIG)
    cursor = cnx.cursor()
    cnx.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username or password is wrong")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        try:
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8mb4'".format(DB_NAME))
            cnx.database = DB_NAME
        except mysql.connector.Error as err:
            print(err.msg)
    else:
        print(err.msg)

try:
    for name, ddl in TABLES.iteritems():
        cursor.execute("DROP TABLE IF EXISTS {}".format(name))
        cursor.execute(ddl)
    for ddl in CREATE_INDEXS:
        cursor.execute(ddl)
except mysql.connector.Error as err:
    print(err.msg)

import csv


def csv_to_mysql(filename, table_structure):
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        try:
            cursor.execute('SET NAMES utf8mb4;')
            cnt = 0
            for row in reader:
                if len(row[2]) > 10:
                    row[2] = '2015' + row[2][row[2].find('-'):-1]
                if cnt == 1597832:
                    row[-1] = row[-1][:row[-1].find('ee7f431c4559bf616ef633869b200aa0') - 1].strip()
                else:
                    row[-1] = row[-1].strip()
                cursor.execute(table_structure, row)
                cnt += 1
            cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)


csv_to_mysql('../weibo_predict_data.txt', add_table2)
csv_to_mysql('../weibo_train_data.txt', add_table1)
csv_to_mysql('../rest.txt', add_table1)

cursor.close()
cnx.close()
