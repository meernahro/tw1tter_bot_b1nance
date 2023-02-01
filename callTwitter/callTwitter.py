import tweepy
from os import getenv
import json
from time import sleep
from datetime import datetime,timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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
    
    tweet = [0,0,0,0]
    


    def on_connect(self):
        print("Twitter Connected")

    def on_data(self, raw_data):
        
        self.local_filter(raw_data)

    def local_filter(self,raw_data):
        parsed_json = json.loads(raw_data)

        try:
            for user in users:
                if users[user]==int(parsed_json['data']['author_id']):
                    self.tweet[0] = user

            self.tweet[1] = parsed_json['data']['text']
            self.tweet[2] = f"https://twitter.com/{self.tweet[0]}/status/{parsed_json['data']['id']}"

            
            time_object = datetime.strptime(parsed_json['data']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            time_object += timedelta(hours=3)
            formatted_time = time_object.strftime("%I:%M %p %d/%m/%Y")

            self.tweet[3] = formatted_time

            sleep(0.5)
            self.send_message_to_group(self.tweet)
        except Exception as e:
            print("Error in Local Filter",e)
        
        

    def send_message_to_group(self,message):

        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(getenv("ROOM_GROUP_NAME"), {"type": "chat_message", "message": message})
            print("callTwitter sent message to group Successfuly")
        
        except Exception as e:
            print("Error sending message to group ",e)




def start_listener():
    listener_obj = Listener(bearer_token=bearer_token)

    rules = listener_obj.get_rules().data
    print(rules)

    # create a new thread for the listener
    tweet_fields = ["author_id","created_at","text"]
    # expansions=["referenced_tweets.id"]
    print("start listener is listeneing")
    listener_obj.filter(tweet_fields=tweet_fields)

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








