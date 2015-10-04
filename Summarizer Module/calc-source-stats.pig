REGISTER mongo-hadoop-1.0.0.jar
REGISTER mongo-hadoop-pig-1.4.0.jar
REGISTER mongo-hadoop-core-1.0.0.jar
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

--- Generate source statistics
source_stats = GROUP norm_tweet BY (tvshow, source);
source_stats = FOREACH source_stats GENERATE group.tvshow as tvshow, group.source as source, COUNT(norm_tweet) AS source_count;
STORE source_stats INTO 'mongodb://127.0.0.1:27017/tvshows.source_stats' USING com.mongodb.hadoop.pig.MongoStorage();

