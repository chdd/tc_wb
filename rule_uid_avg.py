__author__ = 'Des'

import time

import mysql.connector

from mysql.connector import errorcode

from sql_config import *
from weibo_predict_data import WeiboPredictData
from generate_result import generate_result

try:
    cnx = mysql.connector.connect(**DB_CONFIG)
    cnx.database = DB_NAME
    cursor = cnx.cursor()

    cursor.execute(
        "SELECT `AVG(forward_count)`, `AVG(comment_count)`, `AVG(like_count)` FROM features_uid_avg WHERE uid = '0';")
    default_data = cursor.fetchall()

    result = []
    with WeiboPredictData() as weibo_data:
        cnt = 0
        cnt_up = 0
        query = weibo_data.get_all()
        for line in query:

            cnt += 1
            if cnt >= cnt_up:
                print(cnt)
                cnt_up += 1000
                # if cnt > 10: break

            cursor.execute(
                "SELECT `AVG(forward_count)`, `AVG(comment_count)`, `AVG(like_count)` "
                "FROM features_uid_avg WHERE uid = '{}';".format(line[0]))
            data = cursor.fetchall()
            if data:
                result.append(
                    "{0}\t{1}\t{2:.0f},{3:.0f},{4:.0f}\n".format(line[0], line[1], data[0][0], data[0][1], data[0][2]))
            else:
                result.append("{0}\t{1}\t{2:.0f},{3:.0f},{4:.0f}\n".format(line[0], line[1], default_data[0][0],
                                                                           default_data[0][1],
                                                                           default_data[0][2]))

    generate_result('../result/weibo_result' + time.strftime('%m-%d', time.localtime(time.time())) + '.txt', result)

    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print(err.msg)
