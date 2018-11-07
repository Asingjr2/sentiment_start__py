import json

import redis

from tweet import Tweet

class TweetStore:

    redis_host = "localhost"
    redis_port = 6379
    redis_password = ""

    redis_key = "tweets"
    num_tweets = 20

    def __init__(self):
        # Creating connection
        self.db = r = redis.Redis(
            host = self.redis_host,
            port = self.redis_port,
            password = self.redis_password
        )
        self.trim_count = 0

    def push(self, data):
        # Trimming older tweets if older 100
        # Lpush is left push or push in the front of the list (newest first)
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1

        if self.trim_count > 100:
            self.db.ltrim(self.redis_key, 0, self.num_tweets)
            self.trim_count = 0

    def tweets(self, limit=15):
        tweets = []

        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item)
            tweets.append(tweet_obj)

            return tweets

