__author__ = 'Des'

import time

import mysql.connector
from mysql.connector import errorcode

from sql_config import *
from weibo_predict_data import WeiboPredictData
from generate_result import generate_result
from evaluation import precision_rl


def precision_factory(idx, fp, cp, lp, r_list):
    def precision_inner0(p):
        return precision_rl(p, cp, lp, r_list)

    def precision_inner1(p):
        return precision_rl(fp, p, lp, r_list)

    def precision_inner2(p):
        return precision_rl(fp, cp, p, r_list)

    precision_inner = [precision_inner0, precision_inner1, precision_inner2]
    return precision_inner[idx]


def search(idx, fp, cp, lp, m, r_list):
    new_p = [fp, cp, lp]
    precision = precision_factory(idx, fp, cp, lp, r_list)
    large_precision = 0
    for i in range(0, m[idx] + 1):
        temp_precision = precision(i)
        if temp_precision > large_precision:
            large_precision = temp_precision
            new_p[idx] = i
    return new_p[idx], large_precision


def max_precision(r_list):
    fp, cp, lp = 0, 0, 0
    m = [0, 0, 0]
    for i in r_list:
        if i[0] > m[0]:
            m[0] = i[0]
        if i[1] > m[1]:
            m[1] = i[1]
        if i[2] > m[2]:
            m[2] = i[2]
    if len(r_list) == 1:
        return fp, cp, lp

    init_precision = precision_rl(fp, cp, lp, r_list)
    # print '{:.4f}  '.format(init_precision),
    fp, init_precision = search(0, fp, cp, lp, m, r_list)
    # print '{:.4f}  '.format(init_precision),
    cp, init_precision = search(1, fp, cp, lp, m, r_list)
    # print '{:.4f}  '.format(init_precision),
    lp, init_precision = search(2, fp, cp, lp, m, r_list)
    # print '{:.4f}  '.format(init_precision),
    # print

    return fp, cp, lp


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
                uid_map[line[0]] = max_precision(data)

            result.append(
                "{0}\t{1}\t{2:.0f},{3:.0f},{4:.0f}\n".format(line[0], line[1], uid_map[line[0]][0],
                                                             uid_map[line[0]][1], uid_map[line[0]][2]))

    generate_result('../result/weibo_result' + time.strftime('%m-%d', time.localtime(time.time())) + '.txt', result)

    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print(err.msg)
