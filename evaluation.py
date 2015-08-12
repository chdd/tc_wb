__author__ = 'Desmond'


def deviation(predict, real, kind):
    if kind == 'f':
        t = 5.0
    else:
        t = 3.0
    return abs(predict - real) / (real + t)


def precision_i(fp, fr, cp, cr, lp, lr):
    return 1 - 0.5 * deviation(fp, fr, 'f') - 0.25 * deviation(cp, cr, 'c') - 0.25 * deviation(lp, lr, 'l')


def sgn(x):
    if x > 0:
        return 1
    else:
        return 0


def count_i(fr, cr, lr):
    x = fr + cr + lr
    if x > 100:
        return 101
    else:
        return x + 1


def precision(predict_and_real):
    numerator = 0.0
    denominator = 0.0
    for fp, cp, lp, fr, cr, lr in predict_and_real:
        numerator += count_i(fr, cr, lr) * sgn(precision_i(fp, fr, cp, cr, lp, lr) - 0.8)
        denominator += count_i(fr, cr, lr)
    return numerator / denominator * 100
