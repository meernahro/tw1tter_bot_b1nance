import tweepy
from os import getenv
import json
from time import sleep
from datetime import datetime,timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from database_manager import models

from database_manager import models

api_key = getenv("TWITTER_KEY")
api_key_secret = getenv("TWITTER_SECRET")
access_token = getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token,api_key,api_key_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret,access_token,access_token_secret)
api = tweepy.API(auth)

users = {
    "mark_cullen": 0,
    "LukeTradesz": 1,
    "ShardiB2": 2,
    "NahroBarznji": 3,
    "meer_barznji": 4,
    "karl_0x": 5,
    "peach_1340": 6,
    "DarkCryptoLord": 7,
    "NachoTrades": 8
    }
for user in users:
    users[user] = api.get_user(screen_name=user).id   

class Listener(tweepy.StreamingClient):
    
    tweet = [0,0,0,0,0]
    


    def on_connect(self):
        print("Twitter Connected")


# on_data returns this. if tweet is original, full text is returned
# b'{"data":{"author_id":"2833017360","created_at":"2023-02-01T19:00:31.000Z","edit_history_tweet_ids":["1620859659946164225"],"id":"1620859659946164225","text":"Hard to believe that the February 1 terrorist attack was 19 years ago. Heartbreaking to see the lives cut short, their dreams &amp; potential unfulfilled, their families bereft of their love. But easy to believe the people of Kurdistan still stand proud and will never bow to tyranny"},"includes":{"tweets":[{"author_id":"2833017360","created_at":"2023-02-01T19:00:31.000Z","edit_history_tweet_ids":["1620859659946164225"],"id":"1620859659946164225","text":"Hard to believe that the February 1 terrorist attack was 19 years ago. Heartbreaking to see the lives cut short, their dreams &amp; potential unfulfilled, their families bereft of their love. But easy to believe the people of Kurdistan still stand proud and will never bow to tyranny"}]},"matching_rules":[{"id":"1620041380532740096","tag":""}]}'


# on_data returns this. If tweet is retweet
# b'{"data":{"author_id":"2833017360","created_at":"2023-02-01T18:57:14.000Z","edit_history_tweet_ids":["1620858830937812995"],"id":"1620858830937812995","referenced_tweets":[{"type":"retweeted","id":"1620620961015037952"}],"text":"RT @BayanRahman: Hard to believe that the February 1 terrorist attack was 19 years ago. Heartbreaking to see the lives cut short, their dre\xe2\x80\xa6"},"includes":{"tweets":[{"author_id":"2833017360","created_at":"2023-02-01T18:57:14.000Z","edit_history_tweet_ids":["1620858830937812995"],"id":"1620858830937812995","referenced_tweets":[{"type":"retweeted","id":"1620620961015037952"}],"text":"RT @BayanRahman: Hard to believe that the February 1 terrorist attack was 19 years ago. Heartbreaking to see the lives cut short, their dre\xe2\x80\xa6"},{"author_id":"28078770","created_at":"2023-02-01T03:12:01.000Z","edit_history_tweet_ids":["1620620961015037952"],"id":"1620620961015037952","text":"Hard to believe that the February 1 terrorist attack was 19 years ago. Heartbreaking to see the lives cut short, their dreams &amp; potential unfulfilled, their families bereft of their love. But easy to believe the people of Kurdistan still stand proud and will never bow to tyranny https://t.co/IGWnNDssZh"}]},"matching_rules":[{"id":"1620041380532740096","tag":""}]}'


    def on_data(self, raw_data):
        self.extract_tweet_data(raw_data)


    def extract_tweet_data(self,tweet_string):
        try:
            tweet = json.loads(tweet_string)
            data = tweet["data"]
            author_id = data["author_id"]
            created_at = data["created_at"]
            tweet_id = data["id"]
            if "referenced_tweets" in data:
                # tweet is a retweet
                referenced_tweets = data["referenced_tweets"]
                original_tweet = referenced_tweets[0]
                original_tweet_id = original_tweet["id"]
                includes = tweet["includes"]
                original_tweets = includes["tweets"]
                for original_tweet in original_tweets:
                    if original_tweet["id"] == original_tweet_id:
                        full_text = original_tweet["text"]
                        break
            else:
                # tweet is original
                full_text = data["text"]

            for user in users:
                if users[user]==int(author_id):
                    self.tweet[0] = user
            self.tweet[1] = full_text
            self.tweet[2] = f"https://twitter.com/{self.tweet[0]}/status/{tweet_id}"
            time_object = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            time_object += timedelta(hours=3)
            formatted_time = time_object.strftime("%I:%M %p %d/%m/%Y")

            self.tweet[3] = formatted_time
            self.tweet[4] = tweet_id
            print(self.tweet)
            self.send_message_to_group(self.tweet)
        except Exception as e:
            print("Error extracting tweet data",e)

    def send_message_to_group(self,message):

        try:
            # this statement sends the tweet to database
            models.create_tweet(message)
            tweet = models.get_tweet_by_tweet_id(message[4])
            mytweet = [tweet.user,tweet.text,tweet.link,str(tweet.time),tweet.id]
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(getenv("ROOM_GROUP_NAME"), {"type": "chat_message", "message": mytweet})
            print("callTwitter sent message to group Successfuly")
        
        except Exception as e:
            print("Error sending message to group ",e)




def start_listener():
    listener_obj = Listener(bearer_token=bearer_token)
    
    # create a new thread for the listener
    tweet_fields = ["author_id","created_at","text"]
    expansions=["referenced_tweets.id"]
    print("start listener is listeneing")
    listener_obj.filter(tweet_fields=tweet_fields,expansions=expansions)

def follow_user(username):
    try:
        follow_obj = Listener(bearer_token=bearer_token)
        userid = api.get_user(screen_name=username).id
        response = follow_obj.add_rules(tweepy.StreamRule(value=f"from:{userid}"))
        created = response[3]['summary']['created']
        valid = response[3]['summary']['valid']
        if (created==1 and valid ==1):
            return True
        else:
            return False
    except Exception as e:
        print("Error following user",e)

    
    
def get_rule(id):
    get_rule_obj = Listener(bearer_token=bearer_token)
    get_rule_obj.get_rules(id).data

def delete_rule(id):
    delete_rule_obj = Listener(bearer_token=bearer_token)
    delete_rule_obj.delete_rules(id)








