REGISTER mongo-hadoop-1.0.0.jar
REGISTER mongo-hadoop-pig-1.4.0.jar
REGISTER mongo-hadoop-core-1.0.0.jar
--REGISTER mongo-java-driver-2.10.1.jar;
--REGISTER commons-lang3-3.4.jar;
--REGISTER mongo-hadoop-core-1.4.0.jar;
--REGISTER mongo-hadoop-pig-1.4.0.jar;
--REGISTER piggybank.jar;
--REGISTER mongo-hadoop-1.0.0.jar;
--REGISTER elephant-bird-core-4.10.jar;
tweets = LOAD 'mongodb://127.0.0.1:27017/tvshows.tweets' USING com.mongodb.hadoop.pig.MongoLoader(
'favorite_count: long,
id_str: chararray,
lang: chararray,
retweet_count: long,
sentiment: chararray,
source: chararray,
text: chararray,
tvshow: chararray,
user_id_str: chararray',
'mongo_id'
);
users = LOAD 'mongodb://127.0.0.1:27017/tvshows.users' USING com.mongodb.hadoop.pig.MongoLoader(
'description: chararray,
followers_count: long,
gender: chararray,
id_str: chararray,
lang: chararray,
name: chararray,
screen_name: chararray',
'mongo_id'
);

---Generate normalized data
ntweet = JOIN tweets BY user_id_str, users BY id_str;
norm_tweet = FOREACH ntweet GENERATE tweets::id_str as tweet_id, users::id_str as user_id, tweets::favorite_count as fav_count, tweets::lang as lang, tweets::sentiment as sentiment, tweets::source as source, tweets::tvshow as tvshow, users::gender as gender, users::followers_count as followers_count;

---Calculate total count
ntweet = GROUP norm_tweet BY tvshow;
ntweet = FOREACH ntweet GENERATE group, norm_tweet as inner_bag;
s1 = FOREACH ntweet GENERATE group as tvshow, COUNT(inner_bag) as total_count, SUM(inner_bag.fav_count) as fav_count;

---Calculate sentiment wise count
sent_ntweet = GROUP norm_tweet BY (tvshow, sentiment);
summary2 = FOREACH sent_ntweet GENERATE COUNT(norm_tweet) as cnt, group.tvshow as tvshow, group.sentiment as sentiment;
neg_summary2 = FILTER summary2 BY sentiment == 'negative';
pos_summary2 = FILTER summary2 BY sentiment == 'positive';
neu_summary2 = FILTER summary2 BY sentiment == 'neutral';
neg_s2 = FOREACH neg_summary2 GENERATE tvshow, cnt as neg_count;
pos_s2 = FOREACH pos_summary2 GENERATE tvshow, cnt as pos_count;
neu_s2 = FOREACH neu_summary2 GENERATE tvshow, cnt as neu_count;
s2 = JOIN neg_s2 BY tvshow, pos_s2 BY tvshow, neu_s2 BY tvshow;
s2 = FOREACH s2 GENERATE neg_s2::tvshow as tvshow, neg_s2::neg_count as neg_count, pos_s2::pos_count as pos_count, neu_s2::neu_count as neu_count;

--- Aggregrate over gender
gend_ntweet = GROUP norm_tweet BY (tvshow, gender);
gend_ntweet = FOREACH gend_ntweet GENERATE COUNT(norm_tweet) as cnt, group.tvshow as tvshow, group.gender as gender;
male_s3 = FILTER gend_ntweet BY gender == 'male';
female_s3 = FILTER gend_ntweet BY gender == 'female';
andy_s3 = FILTER gend_ntweet BY gender  == 'andy';
male_s3 = FOREACH male_s3 GENERATE tvshow, cnt as male_count;
female_s3 = FOREACH female_s3 GENERATE tvshow, cnt as female_count;
andy_s3 = FOREACH andy_s3 GENERATE tvshow, cnt as andy_count;
s3 = JOIN male_s3 BY tvshow, female_s3 BY tvshow, andy_s3 BY tvshow;
s3 = FOREACH s3 GENERATE male_s3::tvshow as tvshow, male_s3::male_count as male_count, female_s3::female_count as female_count, andy_s3::andy_count as andy_count;

----Aggregate over gender and sentiment
gend_sent = GROUP norm_tweet BY (tvshow, gender, sentiment);
gend_sent = FOREACH gend_sent GENERATE COUNT(norm_tweet) as cnt, group.tvshow as tvshow, group.gender as gender, group.sentiment as sentiment;
male_pos_s4 = FILTER gend_sent BY gender == 'male' AND sentiment == 'positive';
male_neg_s4 = FILTER gend_sent BY gender == 'male' AND sentiment == 'negative';
male_neu_s4 = FILTER gend_sent BY gender == 'male' AND sentiment == 'neutral';
female_pos_s4 = FILTER gend_sent BY gender == 'female' AND sentiment == 'positive';
female_neg_s4 = FILTER gend_sent BY gender == 'female' AND sentiment == 'negative';
female_neu_s4 = FILTER gend_sent BY gender == 'female' AND sentiment == 'neutral';
andy_pos_s4 = FILTER gend_sent BY gender == 'andy' AND sentiment == 'positive';
andy_neg_s4 = FILTER gend_sent BY gender == 'andy' AND sentiment == 'negative';
andy_neu_s4 = FILTER gend_sent BY gender == 'andy' AND sentiment == 'neutral';
s4 = JOIN male_pos_s4 BY tvshow, male_neg_s4 BY tvshow, male_neu_s4 BY tvshow, female_pos_s4 BY tvshow, female_neg_s4 BY tvshow, female_neu_s4 BY tvshow, andy_pos_s4 BY tvshow, andy_neg_s4 BY tvshow, andy_neu_s4 BY tvshow;
s4 = FOREACH s4 GENERATE male_pos_s4::tvshow, male_pos_s4::cnt as male_pos_count, male_neg_s4::cnt as male_neg_count, male_neu_s4::cnt as male_neu_count, female_pos_s4::cnt as female_pos_count, female_neg_s4::cnt as female_neg_count, female_neu_s4::cnt as female_neu_count, andy_pos_s4::cnt as andy_pos_count, andy_neg_s4::cnt as andy_neg_count, andy_neu_s4::cnt as andy_neu_count;

--- Generate reach statistics
reach_norm = FOREACH norm_tweet GENERATE tvshow, user_id, followers_count;
reach_norm = DISTINCT reach_norm;
reach_stats = GROUP reach_norm BY tvshow;
reach_stats = FOREACH reach_stats GENERATE group as tvshow, SUM(reach_norm.followers_count) as reach;
s5 = FOREACH reach_stats GENERATE tvshow, reach;


---- Generate language statistics
lang_stats = GROUP norm_tweet BY (tvshow, lang);
lang_stats = FOREACH lang_stats GENERATE group.tvshow as tvshow, group.lang as lang, COUNT(norm_tweet) AS lang_count;

--- Generate source statistics
source_stats = GROUP norm_tweet BY (tvshow, source);
source_stats = FOREACH source_stats GENERATE group.tvshow as tvshow, group.source as source, COUNT(norm_tweet) AS source_count;

--- Combine summaries
s = JOIN s1 by tvshow, s2 by tvshow, s3 by tvshow, s4 by tvshow, s5 by tvshow;
s = FOREACH s GENERATE s1::tvshow as tvshow, s1::total_count as total_count, s1::fav_count as fav_count, s2::pos_count as pos_count, s2::neg_count as neg_count, s2::neu_count as neu_count, s3::male_count as male_count, s3::female_count as female_count, s3::andy_count as andy_count, s4::male_pos_count as male_pos_count, s4::male_neg_count as male_neg_count, s4::male_neu_count as male_neu_count, s4::female_pos_count as female_pos_count, s4::female_neg_count as female_neg_count, s4::female_neu_count as female_neu_count, s4::andy_pos_count as andy_pos_count, s4::andy_neg_count as andy_neg_count, s4::andy_neu_count as andy_neu_count, s5::reach as reach;

DUMP s;
DUMP lang_stats;
DUMP source_stats;

--- Store into mongo
STORE s INTO 'mongodb://127.0.0.1:27017/tvshows.all_stats' USING com.mongodb.hadoop.pig.MongoStorage();
STORE lang_stats INTO 'mongodb://127.0.0.1:27017/tvshows.lang_stats' USING com.mongodb.hadoop.pig.MongoStorage();
STORE source_stats INTO 'mongodb://127.0.0.1:27017/tvshows.source_stats' USING com.mongodb.hadoop.pig.MongoStorage();
