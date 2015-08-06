__author__ = 'Desmond'

import csv

import mysql.connector
from mysql.connector import errorcode

from sql_config import *


def csv_to_mysql(cur, filename, table_structure):
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        try:
            cur.execute('SET NAMES utf8mb4;')
            cnt = 0
            for row in reader:
                if len(row[2]) > 10:
                    row[2] = '2015' + row[2][row[2].find('-'):-1]
                if cnt == 1597832:
                    row[-1] = row[-1][:row[-1].find('ee7f431c4559bf616ef633869b200aa0') - 1].strip()
                else:
                    row[-1] = row[-1].strip()
                cur.execute(table_structure, row)
                cnt += 1
            cnx.commit()
        except mysql.connector.Error as err0:
            print(err0.msg)


table1 = "weibo_train_data"
TABLES = {table1: (
    "CREATE TABLE IF NOT EXISTS `{}` ("
    "`uid` char(32) NOT NULL,"
    "`mid` char(32) NOT NULL,"
    "`time` date NOT NULL,"
    "`forward_count` int NOT NULL,"
    "`comment_count` int NOT NULL,"
    "`like_count` int NOT NULL,"
    "`content` text NOT NULL"
    ") ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;".format(table1)
)}

add_table1 = ("INSERT INTO `{}` "
              "(uid, mid, time, forward_count, comment_count, like_count, content) "
              "VALUES (%s, %s, %s, %s, %s, %s, %s)".format(table1))

table2 = "weibo_predict_data"
TABLES[table2] = (
    "CREATE TABLE IF NOT EXISTS `{}` ("
    "`uid` char(32) NOT NULL,"
    "`mid` char(32) NOT NULL,"
    "`time` date NOT NULL,"
    "`content` text NOT NULL"
    ") ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;".format(table2)
)

add_table2 = ("INSERT INTO {} "
              "(uid, mid, time, content) "
              "VALUES (%s, %s, %s, %s)".format(table2))

CREATE_INDEXS = [
    "ALTER TABLE `{}` ADD INDEX(`uid`);".format(table1),
    "ALTER TABLE `{}` ADD INDEX(`time`);".format(table1),
    "ALTER TABLE `{}` ADD INDEX(`mid`);".format(table1),
    "ALTER TABLE `{}` ADD INDEX(`uid`);".format(table2),
    "ALTER TABLE `{}` ADD INDEX(`time`);".format(table2),
    "ALTER TABLE `{}` ADD INDEX(`mid`);".format(table2)]

try:
    cnx = mysql.connector.connect(**DB_CONFIG)
    cursor = cnx.cursor()
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8mb4'".format(DB_NAME))
    cnx.database = DB_NAME

    for name, ddl in TABLES.iteritems():
        cursor.execute("DROP TABLE IF EXISTS {}".format(name))
        cursor.execute(ddl)
    for ddl in CREATE_INDEXS:
        cursor.execute(ddl)

    csv_to_mysql(cursor, '../weibo_predict_data.txt', add_table2)  # 274805
    csv_to_mysql(cursor, '../weibo_train_data.txt', add_table1)  # 1623522
    csv_to_mysql(cursor, '../rest.txt', add_table1)

    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    print(err.msg)
