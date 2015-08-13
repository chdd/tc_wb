__author__ = 'Des'

import mysql.connector
from mysql.connector import errorcode
import numpy as np
from sklearn import linear_model, svm
from sklearn.metrics import f1_score

from sql_config import *
from evaluation import precision

train_num = 10000
test_num = 10000
train_set = []
try:
    cnx = mysql.connector.connect(**DB_CONFIG)
    cnx.database = DB_NAME
    cursor = cnx.cursor()

    cursor.execute(
        "SELECT uid_af, uid_ac, uid_al, "  # uid_send, uid_sf, uid_sc, uid_asl,
        "tags_af, tags_ac, tags_al, "  # tags_mf, tags_mc, tags_ml, tags_sf, tags_sc, tags_sl,
        "forward_count, comment_count, like_count FROM train_set ORDER BY rand() LIMIT {}".format(train_num + test_num))
    train_set = np.array(cursor.fetchall())

    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print(err.msg)


# Split the data into training/testing sets
C_X_train = train_set[:train_num, :-3]
C_X_test = train_set[train_num:, :-3]

# Split the targets into training/testing sets
C_y_train = train_set[:train_num, -1] + train_set[:train_num, -2] + train_set[:train_num, -3]
C_y_test = train_set[train_num:, -1] + train_set[train_num:, -2] + train_set[train_num:, -3]
C_y_train = [1 if y > 0 else 0 for y in C_y_train]
C_y_test = [1 if y > 0 else 0 for y in C_y_test]

clf = svm.SVC()
clf.fit(C_X_train, C_y_train)
y_predict = clf.predict(C_X_test)
print f1_score(C_y_test, y_predict)

# Split the targets into training/testing sets
y_train = train_set[:train_num, -3:]
y_test = train_set[train_num:, -3:]

X_train = []
f_y_train = []
c_y_train = []
l_y_train = []
for i in range(0, len(C_y_train)):
    if C_y_train[i] == 1:
        X_train.append(C_X_train[i])
        f_y_train.append(y_train[i][0])
        c_y_train.append(y_train[i][1])
        l_y_train.append(y_train[i][2])

X_test = []
f_y_test = []
c_y_test = []
l_y_test = []
for i in range(0, len(y_predict)):
    if y_predict[i] == 1:
        X_test.append(C_X_test[i])
        f_y_test.append(y_test[i][0])
        c_y_test.append(y_test[i][1])
        l_y_test.append(y_test[i][2])

# Create linear regression object
f_regr = linear_model.LinearRegression()
c_regr = linear_model.LinearRegression()
l_regr = linear_model.LinearRegression()

# Train the model using the training sets
f_regr.fit(X_train, f_y_train)
c_regr.fit(X_train, c_y_train)
l_regr.fit(X_train, l_y_train)

f_y_predict = f_regr.predict(X_test).tolist()
c_y_predict = c_regr.predict(X_test).tolist()
l_y_predict = l_regr.predict(X_test).tolist()

# The coefficients
print('Coefficients: \n')
print f_regr.coef_
print c_regr.coef_
print l_regr.coef_
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % f_regr.score(X_test, f_y_test))
print('Variance score: %.2f' % c_regr.score(X_test, c_y_test))
print('Variance score: %.2f' % l_regr.score(X_test, l_y_test))

for i in range(0, len(y_predict)):
    if y_predict[i] == 0:
        f_y_test.append(y_test[i][0])
        c_y_test.append(y_test[i][1])
        l_y_test.append(y_test[i][2])
        f_y_predict.append(0)
        c_y_predict.append(0)
        l_y_predict.append(0)

predict_and_real = []
for i in range(0, len(y_predict)):
    predict_and_real.append([f_y_predict[i], c_y_predict[i], l_y_predict[i], f_y_test[i], c_y_test[i], l_y_test[i]])

predict_and_real0 = []
for i in range(0, len(y_predict)):
    predict_and_real0.append([0, 0, 0, f_y_test[i], c_y_test[i], l_y_test[i]])

print(len(y_predict))
print "Predict: {:.2f}%".format(precision(predict_and_real))
print "Zero baseline: {:.2f}%".format(precision(predict_and_real0))
