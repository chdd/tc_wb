__author__ = 'Desmond'

import jieba
import jieba.analyse
import jieba.posseg

from weibo_train_data import WeiboTrainData


def get_train_data_features(WeiboData):
    with WeiboData() as weibo_data:

        k = 30
        is_with_weight = True
        pos = ('n', 'r', 'nr', 'ns', 'vn', 'v')

        query = weibo_data.exe("SELECT * FROM " + weibo_data.table_name + " ORDER BY forward_count DESC LIMIT 0, 100")
        for line in query:
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
                if tag[0] in tags_dict:
                    tags_dict[tag[0]][1] = tag[1]
                else:
                    tags_dict[tag[0]] = [0, tag[1]]

            print line[1], line[2]
            if len(line) > 4:
                print line[3], line[4], line[5]
            print line[-1]
            for tag, val in tags_dict.iteritems():
                print tag, val[0], val[1]
            print


get_train_data_features(WeiboTrainData)  # 15314770
# get_train_data_features(WeiboPredictData)
