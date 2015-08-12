__author__ = 'Des'

import mysql.connector
from mysql.connector import errorcode
import numpy as np
from sklearn import linear_model

from sql_config import *
from evaluation import precision

train_num = 100000
test_num = 100000
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
X_train = train_set[:train_num, :-3]
X_test = train_set[train_num:, :-3]

# Split the targets into training/testing sets
f_y_train = train_set[:train_num, -3]
f_y_test = train_set[train_num:, -3]
c_y_train = train_set[:train_num, -2]
c_y_test = train_set[train_num:, -2]
l_y_train = train_set[:train_num, -1]
l_y_test = train_set[train_num:, -1]

# Create linear regression object
f_regr = linear_model.LinearRegression()
c_regr = linear_model.LinearRegression()
l_regr = linear_model.LinearRegression()

# Train the model using the training sets
f_regr.fit(X_train, f_y_train)
c_regr.fit(X_train, c_y_train)
l_regr.fit(X_train, l_y_train)

f_y_predict = f_regr.predict(X_test)
c_y_predict = c_regr.predict(X_test)
l_y_predict = l_regr.predict(X_test)

# The coefficients
print('Coefficients: \n')
print f_regr.coef_
print c_regr.coef_
print l_regr.coef_
# The mean square error
print("Residual sum of squares: %.2f" % np.mean((f_y_predict - f_y_test) ** 2))
print("Residual sum of squares: %.2f" % np.mean((c_y_predict - c_y_test) ** 2))
print("Residual sum of squares: %.2f" % np.mean((l_y_predict - l_y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % f_regr.score(X_test, f_y_test))
print('Variance score: %.2f' % c_regr.score(X_test, c_y_test))
print('Variance score: %.2f' % l_regr.score(X_test, l_y_test))

predict_and_real = []
for i in range(0, test_num):
    predict_and_real.append([f_y_predict[i], c_y_predict[i], l_y_predict[i], f_y_test[i], c_y_test[i], l_y_test[i]])

predict_and_real0 = []
for i in range(0, test_num):
    predict_and_real0.append([0, 0, 0, f_y_test[i], c_y_test[i], l_y_test[i]])

print "Predict: {:.2f}%".format(precision(predict_and_real))
print "Zero baseline: {:.2f}%".format(precision(predict_and_real0))
