from pymongo import MongoClient
import collections

client = MongoClient()
db = client.colaSuperBowl

retweeted_dict = collections.defaultdict(list)
no_retweeted_list = []
for document in db.rlvtPosts.find({"source_type": "twitter"}):
	post_id = document["ds_twitter__id"]
	retweeted_key = "ds_twitter__retweeted__id"
	if retweeted_key in document:
		retweeted_dict[document[retweeted_key]].append(post_id)
	else:
		no_retweeted_list.append(post_id)

original_tweet_list = []
no_original_tweet_list = []
deputy_original_tweet_dict = collections.defaultdict(int)
for key in retweeted_dict.keys():
	if key in no_retweeted_list:
		#print key
		original_tweet_list.append(key)
		no_retweeted_list.remove(key)
	else:
		no_original_tweet_list.append(key)
		deputy_original_tweet_dict[retweeted_dict[key][0]] = len(retweeted_dict[key])


#print len(retweeted_dict)
print len(original_tweet_list)
#print len(no_original_tweet_list)
#print no_original_tweet_list
print len(deputy_original_tweet_dict)
#print deputy_original_tweet_dict
print len(no_retweeted_list)

ct1 = 0
ct2 = 0
ct3 = 0
for document in db.rlvtPosts.find({"source_type": "twitter"}):
	post_id = document["ds_twitter__id"]
	retweeted_key = "ds_twitter__retweeted__id"
	# find original tweet and accumulate retweets
	if post_id in original_tweet_list:
		# taking into account of the orignal tweet
		document["retweets_count"] = len(retweeted_dict[post_id]) + 1
		db.tweetsCleaned.insert(document)
		ct1 += 1
	if post_id in deputy_original_tweet_dict.keys():
		# no original tweet, so no plus one
		document["retweets_count"] = deputy_original_tweet_dict[post_id]
		db.tweetsCleaned.insert(document)
		ct2 += 1
	if post_id in no_retweeted_list:
		db.tweetsCleaned.insert(document)
		ct3 += 1

print ct1, ct2, ct3





