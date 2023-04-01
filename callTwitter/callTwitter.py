import tweepy
from os import getenv
import json
from time import sleep
from datetime import datetime,timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from database_manager import models


from analyze_tweet.analyze_tweet import TweetAnalyzer
import threading

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
    "__bleeker":1,
    "ShardiB2": 2,
    "NahroBarznji": 3,
    "meer_barznji": 4,
    "karl_0x": 5,
    "peach_1340": 6,
    "DarkCryptoLord": 7,
    "NachoTrades": 8
    }


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

            my_user_name = models.get_User_by_id(author_id).user_name
            
            self.tweet[0] = my_user_name
            self.tweet[1] = full_text
            self.tweet[2] = f"https://twitter.com/{self.tweet[0]}/status/{tweet_id}"
            time_object = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            time_object += timedelta(hours=3)
            formatted_time = time_object.strftime("%I:%M %p %d/%m/%Y")

            self.tweet[3] = formatted_time
            self.tweet[4] = tweet_id
            self.send_message_to_group(self.tweet)
        except Exception as e:
            print("Error: Line 95 callTwitter",e)

    def send_message_to_group(self,message):
        
        try:
            
            # this statement sends the tweet to database
            models.create_tweet(message)
            tweet = models.get_tweet_by_tweet_id(message[4])
            
            name = tweet.user.user_name
            print(name)
            formatted_time = tweet.time.strftime("%I:%M %p %d/%m/%Y")
            mytweet = [name,tweet.text,tweet.link,formatted_time,tweet.id]

            token_obj = TweetAnalyzer(tweet.id)
            analyze_thread = threading.Thread(target=token_obj.analyze)
            analyze_thread.start()
            print("analyze_thread started")
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(getenv("ROOM_GROUP_NAME"), {"type": "chat_message", "message": mytweet})
            print("callTwitter sent message to group Successfuly")
        
        except Exception as e:
            print("Error: Line 119 callTwitter",e)


obj = Listener(bearer_token=bearer_token)

def start_listener():
    # listener_obj = Listener(bearer_token=bearer_token)
    
    # create a new thread for the listener
    tweet_fields = ["author_id","created_at","text"]
    expansions=["referenced_tweets.id"]
    
    obj.filter(tweet_fields=tweet_fields,expansions=expansions)
    
    print("start listener is listeneing")

def follow_user(username):
    try:
        # follow_obj = Listener(bearer_token=bearer_token)
        userid = api.get_user(screen_name=username).id
        response = obj.add_rules(tweepy.StreamRule(value=f"from:{userid}"))
        print(userid)
        print(response)
        created = response[3]['summary']['created']
        valid = response[3]['summary']['valid']
        rule_id = response.data[0].id
        print(rule_id)
        print(created)
        print(valid)
        if (created==1 and valid ==1):
            models.create_User(username,userid)
            models.create_Rule(rule_id,username)
            return True
        else:
            return False
    except Exception as e:
        print("Error: Line 155 callTwitter",e)
        # response=Response(data=[StreamRule(value='from:1518981537307496448', tag=None, id='1626494120624619522')], includes={}, errors=[], meta={'sent': '2023-02-17T08:09:52.932Z', 'summary': {'created': 1, 'not_created': 0, 'valid': 1, 'invalid': 0}})

    
    
def get_rule(id):
    # get_rule_obj = Listener(bearer_token=bearer_token)
    return obj.get_rules(id)

def get_rule():
    # get_rule_obj = Listener(bearer_token=bearer_token)
    return obj.get_rules()

def delete_rule(id):
    # delete_rule_obj = Listener(bearer_token=bearer_token)
    obj.delete_rules(id)
    models.delete_Rule_by_id(id)

def unfollow_user(username):
    try:
        rule_id = models.get_rule_by_user(username)
        obj.delete_rules(rule_id)

    except Exception as e:
        print("Error: Line 179 callTwitter",e)

