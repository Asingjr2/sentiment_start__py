import json
import datetime

from textblob import TextBlob
import tweepy as tw

from tweet_store import TweetStore

file_path = "../redis_tweet/<your_path>"
# file_path = "../<your-directory>/api_keys.txt"

with open(file_path) as f:
    access_info = json.loads(f.read())

auth = tw.OAuthHandler(access_info["<your_key>"], access_info["<your_secret"])
auth.set_access_token(access_info["<your_token>"], access_info["<your_token_secert"])

api = tw.API(auth)
store = TweetStore()

class Listener(tw.StreamListener):

    def on_status(self, status):
        # Check full tweet response type and fields
        blob = TextBlob(status.text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity

        if ("RT @" not in status.text):
            tweet_item = {
                "id_str" : status.id_str,
                "text" : status.text,
                "polarity" : polarity,
                "subjectivity" : subjectivity,
                "username" : status.user.screen_name,
                "name" : status.user.name,
                "profile_image_url" : status.user.profile_image_url,
                "received_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # store.push(tweet_item)
            print("pushed to redis: ", tweet_item)
    
    def on_error(self, status_code):
        # 420 is equivalent to rate limit status
        if status_code == 420:
            return False

stream_listener = Listener()
stream = tw.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["football"])
