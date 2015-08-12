
DROP TABLE IF EXISTS train_set;
CREATE TABLE IF NOT EXISTS train_set  ENGINE=MYISAM DEFAULT CHARSET=UTF8MB4 SELECT tta.*,
    ttb.`COUNT(uid)` AS uid_send,
    ttb.`AVG(forward_count)` AS uid_af,
    ttb.`AVG(comment_count)` AS uid_ac,
    ttb.`AVG(like_count)` AS uid_al,
    ttb.`STD(forward_count)` AS uid_sf,
    ttb.`STD(comment_count)` AS uid_sc,
    ttb.`STD(like_count)` AS uid_asl FROM
    (SELECT
        t.uid,
		t.mid,
		t.content,
		t.forward_count,
		t.comment_count,
		t.like_count,
		MAX(tag_mf) AS tags_mf,
		MAX(tag_mc) AS tags_mc,
		MAX(tag_ml) AS tags_ml,
		AVG(tag_af) AS tags_af,
		AVG(tag_ac) AS tags_ac,
		AVG(tag_al) AS tags_al,
		AVG(tag_sf) AS tags_sf,
		AVG(tag_sc) AS tags_sc,
		AVG(tag_sl) AS tags_sl
    FROM
        (SELECT
        ta.uid,
		ta.mid,
		ta.content,
		ta.forward_count,
		ta.comment_count,
		ta.like_count,
		tc.`MAX(forward_count)` AS tag_mf,
		tc.`MAX(comment_count)` AS tag_mc,
		tc.`MAX(like_count)` AS tag_ml,
		tc.`AVG(forward_count)` AS tag_af,
		tc.`AVG(comment_count)` AS tag_ac,
		tc.`AVG(like_count)` AS tag_al,
		tc.`STD(forward_count)` AS tag_sf,
		tc.`STD(comment_count)` AS tag_sc,
		tc.`STD(like_count)` AS tag_sl
    FROM
        weibo_train_data AS ta
    INNER JOIN features_tags AS tb ON ta.mid = tb.mid
    JOIN tags_avg_fcl_count AS tc ON tb.tag = tc.tag) AS t
    GROUP BY t.mid) AS tta
        JOIN
    features_uid_avg AS ttb ON tta.uid = ttb.uid;
