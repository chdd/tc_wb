--270812
--CREATE TABLE IF NOT EXISTS tag SELECT COUNT(DISTINCT tag) FROM features_tags;

DROP TABLE IF EXISTS tags_avg_fcl_count;
CREATE TABLE IF NOT EXISTS tags_avg_fcl_count  ENGINE=MYISAM DEFAULT CHARSET=UTF8MB4 SELECT tag,
    COUNT(tag),
    SUM(forward_count),
    SUM(comment_count),
    SUM(like_count),
    MAX(forward_count),
    MAX(comment_count),
    MAX(like_count),
    AVG(forward_count),
    AVG(comment_count),
    AVG(like_count),
    STD(forward_count),
    STD(comment_count),
    STD(like_count) FROM
    (SELECT
        ta.tag,
            tb.forward_count,
            tb.comment_count,
            tb.like_count
    FROM
        features_tags AS ta
    JOIN weibo_train_data AS ttb ON tta.mid = ttb.mid) AS tt
GROUP BY tag;