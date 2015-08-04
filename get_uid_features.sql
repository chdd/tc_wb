--uid 24759 45582 inner 23521
SELECT
    COUNT(DISTINCT uid)
FROM
    weibo_predict_data;

SELECT
    COUNT(DISTINCT uid)
FROM
    weibo_train_data;

SELECT
    COUNT(a.uid)
FROM
    (SELECT DISTINCT
        uid
    FROM
        weibo_predict_data) AS a
        JOIN
    (SELECT DISTINCT
        uid
    FROM
        weibo_train_data) AS b ON a.uid = b.uid;

DROP TABLE IF EXISTS features_uid_avg;
CREATE TABLE IF NOT EXISTS features_uid_avg  ENGINE=MYISAM DEFAULT CHARSET=UTF8MB4 SELECT uid,
    COUNT(uid),
    AVG(forward_count),
    AVG(comment_count),
    AVG(like_count),
    STD(forward_count),
    STD(comment_count),
    STD(like_count)
FROM
    weibo_train_data
GROUP BY uid;
    
INSERT INTO features_uid_avg 
	SELECT 
    '0',
    COUNT(uid) / COUNT(DISTINCT uid),
    AVG(forward_count),
    AVG(comment_count),
    AVG(like_count),
    STD(forward_count),
    STD(comment_count),
    STD(like_count)
FROM
    weibo_train_data;