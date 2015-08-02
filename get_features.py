__author__ = 'Desmond'

import cPickle as Pickle

import jieba
import jieba.analyse
import jieba.posseg

from weibo_predict_data import WeiboPredictData
from weibo_train_data import WeiboTrainData


def get_content_tags(file_name, WeiboData):
    with WeiboData() as weibo_data:

        k = 30
        is_with_weight = True
        pos = ('n', 'r', 'nr', 'ns', 'vn', 'v')

        cnt = 0
        cnt_up = 0
        DEBUG = False
        mid_tags_dict = {}
        for line in weibo_data.gen_all():
            cnt += 1
            if cnt >= cnt_up:
                print(cnt)
                cnt_up += 1000

            if DEBUG:
                if cnt < 10:
                    continue
                if cnt > 20:
                    break

            # type1
            tags_idf = jieba.analyse.extract_tags(line[-1], topK=k, withWeight=is_with_weight,
                                                  allowPOS=pos)
            # type2
            tags_text_rank = jieba.analyse.textrank(line[-1], topK=k, withWeight=is_with_weight,
                                                    allowPOS=pos)

            tags_dict = {}
            for tag in tags_idf:
                tags_dict[tag[0]] = [tag[1], 0]
            for tag in tags_text_rank:
                if tags_dict.has_key(tag[0]):
                    tags_dict[tag[0]][1] = tag[1]
                else:
                    tags_dict[tag[0]] = [0, tag[1]]
            mid_tags_dict[line[1]] = tags_dict

            if DEBUG:
                print(line[-1])
                if is_with_weight is True:
                    for tag in tags_idf:
                        print("%s\t%f" % (tag[0], tag[1]))
                    print '-----'
                    for tag in tags_text_rank:
                        print("%s\t%f" % (tag[0], tag[1]))
                else:
                    print(", ".join(tags_idf))
                    print(", ".join(tags_text_rank))
                print
        with open(file_name, 'w') as f:
            Pickle.dump(mid_tags_dict, f)


get_content_tags("..\\predict_data_tags.pkl", WeiboPredictData)
get_content_tags("..\\train_data_tags.pkl", WeiboTrainData)

# with open("..\\predict_data_tags.pkl", 'r') as f:
#     tags = Pickle.load(f)
#     for mid, val in tags.iteritems():
#         print(mid)
#         for tag, conf in val.iteritems():
#             print("%s\t%f\t%f" % (tag, conf[0], conf[1]))
#         print
