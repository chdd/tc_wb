-- 1051502
SELECT count(mid) FROM weibo_train_data WHERE forward_count = 0 AND comment_count = 0 AND like_count = 0;

-- 1409461
SELECT count(mid) FROM weibo_train_data WHERE forward_count < 5 AND comment_count < 3 AND like_count < 3;
