__author__ = 'Des'

import time

import mysql.connector
from mysql.connector import errorcode

from sql_config import *
from weibo_predict_data import WeiboPredictData
from generate_result import generate_result
from evaluation import precision_rl


def median(my_list):
    sorts = sorted(my_list)
    length = len(sorts)
    # print length
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2
    return sorts[length / 2]


def search(idx, down, new_p, r_list):
    last_precision = 0
    while True:
        if down:
            new_p[idx] -= 1
        else:
            new_p[idx] += 1
        temp_precision = precision_rl(new_p[0], new_p[1], new_p[2], r_list)
        if temp_precision > last_precision:
            last_precision = temp_precision
        else:
            if down:
                new_p[idx] += 1
            else:
                new_p[idx] -= 1
            break
    return new_p[idx], last_precision


def search_two_sides(idx, fp, cp, lp, r_list, init_precision):
    new_p = [fp, cp, lp]
    dp, dp_precision = search(idx, True, new_p, r_list)
    up, up_precision = search(idx, False, new_p, r_list)
    if dp_precision > init_precision or up_precision > init_precision:
        if dp_precision > up_precision:
            return dp, dp_precision
        else:
            return up, up_precision
    return new_p[idx], init_precision


def max_precision(r_list):
    fr_list, cr_list, lr_list = [], [], []
    N = len(r_list)
    for i in r_list:
        fr_list.append(i[0])
        cr_list.append(i[1])
        lr_list.append(i[2])
    # fp, cp, lp = median(fr_list), median(cr_list), median(lr_list
    fp, cp, lp = sum(fr_list) / N, sum(cr_list) / N, sum(lr_list) / N

    if len(r_list) == 1:
        return fp, cp, lp

    init_precision = precision_rl(fp, cp, lp, r_list)
    # print '{:.4f}  '.format(init_precision),
    fp, init_precision = search_two_sides(0, fp, cp, lp, r_list, init_precision)
    # print '{:.4f}  '.format(init_precision),
    cp, init_precision = search_two_sides(1, fp, cp, lp, r_list, init_precision)
    # print '{:.4f}  '.format(init_precision),
    lp, init_precision = search_two_sides(2, fp, cp, lp, r_list, init_precision)
    # print '{:.4f}  '.format(init_precision),
    #
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
