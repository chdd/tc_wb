__author__ = 'Des'

import math

import mysql.connector

from mysql.connector import errorcode

from sql_config import *
from evaluation import precision


def median(my_list):
    sorts = sorted(my_list)
    length = len(sorts)
    # print length
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]


train_num = 100000
test_num = 300000

try:
    cnx = mysql.connector.connect(**DB_CONFIG)
    cnx.database = DB_NAME
    cursor = cnx.cursor()

    # cursor.execute(
    #     "SELECT uid, forward_count, comment_count, like_count "
    #     "FROM weibo_train_data WHERE time < '2014-12-01' ORDER BY rand() LIMIT {}".format(train_num))
    # train_set = np.array(cursor.fetchall())

    cursor.execute(
        "SELECT uid, forward_count, comment_count, like_count "
        "FROM weibo_train_data WHERE time >= '2014-12-01' ORDER BY rand() LIMIT {}".format(test_num))
    test_set = cursor.fetchall()

    predict_and_real_med = []
    predict_and_real_avg = []
    predict_and_real_std = []
    predict_and_real_0_baseline = []
    med_map = {}
    avg_map = {}
    std_map = {}
    cnt = 0
    cnt_up = 0
    for line in test_set:

        cnt += 1
        if cnt >= cnt_up:
            print(cnt)
            cnt_up += 1000
            # if cnt > 10: break

        uid = line[0]
        if uid not in med_map:
            cursor.execute(
                "SELECT forward_count, comment_count, like_count "
                "FROM `weibo_train_data` WHERE uid = '{}' AND time < '2014-12-01';".format(uid))
            data = cursor.fetchall()
            if not data:
                data = [[0, 0, 0]]
            N = len(data)
            fc_list = []
            cc_list = []
            lc_list = []
            for i in data:
                fc_list.append(i[0])
                cc_list.append(i[1])
                lc_list.append(i[2])
            med_map[uid] = [median(fc_list), median(cc_list), median(lc_list)]
            avg_map[uid] = [sum(fc_list) / N, sum(cc_list) / N, sum(lc_list) / N]

            f_sum2 = 0.0
            c_sum2 = 0.0
            l_sum2 = 0.0
            for i in range(N):
                f_sum2 += fc_list[i] ** 2
                c_sum2 += cc_list[i] ** 2
                l_sum2 += lc_list[i] ** 2
            f_std = math.sqrt(f_sum2 / N - avg_map[uid][0] ** 2)
            c_std = math.sqrt(c_sum2 / N - avg_map[uid][1] ** 2)
            l_std = math.sqrt(l_sum2 / N - avg_map[uid][2] ** 2)
            std_map[uid] = [f_std, c_std, l_std]

        predict_and_real_med.append([med_map[uid][0], med_map[uid][1], med_map[uid][2], line[1], line[2], line[3]])
        predict_and_real_avg.append([avg_map[uid][0], avg_map[uid][1], avg_map[uid][2], line[1], line[2], line[3]])
        predict_and_real_std.append([med_map[uid][0], med_map[uid][1], med_map[uid][2], line[1], line[2], line[3]])
        std_thres = 5
        if std_map[uid][0] > std_thres and 0 < predict_and_real_std[-1][0]:
            predict_and_real_std[-1][0] += 5
        if std_map[uid][1] > std_thres and 0 < predict_and_real_std[-1][1]:
            predict_and_real_std[-1][1] += 5
        if std_map[uid][2] > std_thres and 0 < predict_and_real_std[-1][2]:
            predict_and_real_std[-1][2] += 5

        predict_and_real_0_baseline.append([0, 0, 0, line[1], line[2], line[3]])

        # print(predict_and_real_med[-1])

    print "Median predict: {:.2f}%".format(precision(predict_and_real_med))
    print "Average predict: {:.2f}%".format(precision(predict_and_real_avg))
    print "Median and STD predict: {:.2f}%".format(precision(predict_and_real_std))
    print "Zero baseline: {:.2f}%".format(precision(predict_and_real_0_baseline))

    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print(err.msg)
