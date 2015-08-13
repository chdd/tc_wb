__author__ = 'Des'

import time

import mysql.connector
from mysql.connector import errorcode

from sql_config import *
from weibo_predict_data import WeiboPredictData
from generate_result import generate_result


def median(my_list):
    sorts = sorted(my_list)
    length = len(sorts)
    # print length
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]


try:
    cnx = mysql.connector.connect(**DB_CONFIG)
    cnx.database = DB_NAME
    cursor = cnx.cursor()

    result = []
    with WeiboPredictData() as weibo_data:
        cnt = 0
        cnt_up = 0
        query = weibo_data.get_all()
        uid_map = {}
        for line in query:

            cnt += 1
            if cnt >= cnt_up:
                print(cnt)
                cnt_up += 1000
                # if cnt > 10: break

            if line[0] not in uid_map:
                cursor.execute(
                    "SELECT forward_count, comment_count, like_count "
                    "FROM `weibo_train_data` WHERE uid = '{}';".format(line[0]))
                data = cursor.fetchall()
                if not data:
                    data = [[0, 0, 0]]
                fc_med = []
                cc_med = []
                lc_med = []
                for i in data:
                    fc_med.append(i[0])
                    cc_med.append(i[1])
                    lc_med.append(i[2])
                uid_map[line[0]] = [median(fc_med), median(cc_med), median(lc_med)]

            result.append(
                "{0}\t{1}\t{2:.0f},{3:.0f},{4:.0f}\n".format(line[0], line[1], uid_map[line[0]][0],
                                                             uid_map[line[0]][1], uid_map[line[0]][2]))

    generate_result('../result/weibo_result' + time.strftime('%m-%d', time.localtime(time.time())) + '.txt', result)

    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print(err.msg)
