import tweepy
from os import getenv
import json
from time import sleep
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from database_manager import models
from analyze_tweet.analyze_tweet import TweetAnalyzer
import threading

# Twitter API credentials
api_key = getenv("TWITTER_KEY")
api_key_secret = getenv("TWITTER_SECRET")
access_token = getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = getenv("TWITTER_BEARER_TOKEN")

# Create a Tweepy Client
client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)

# Create an OAuth1UserHandler and API instance
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Dictionary of users and their indices
users = {
    "mark_cullen": 0,
    "__bleeker": 1,
    "ShardiB2": 2,
    # ... add more users
}

class Listener(tweepy.StreamingClient):
    """
    Custom streaming listener to process and analyze Twitter data.
    """

    tweet = [0, 0, 0, 0, 0]

    def on_connect(self):
        print("Twitter Connected")

    def on_data(self, raw_data):
        self.extract_tweet_data(raw_data)

    def extract_tweet_data(self, tweet_string):
        try:
            tweet = json.loads(tweet_string)
            data = tweet["data"]
            author_id = data["author_id"]
            created_at = data["created_at"]
            tweet_id = data["id"]
            # ... continue extracting data
            
            self.send_message_to_group(self.tweet)
        except Exception as e:
            print("Error: Line 95 callTwitter", e)
    
    def send_message_to_group(self, message):
        try:
            # ... process and send the message
        except Exception as e:
            print("Error: Line 119 callTwitter", e)

# Create a Listener instance
obj = Listener(bearer_token=bearer_token)

# Function to start the listener
def start_listener():
    tweet_fields = ["author_id", "created_at", "text"]
    expansions = ["referenced_tweets.id"]
    obj.filter(tweet_fields=tweet_fields, expansions=expansions)

# Function to follow a user's tweets
def follow_user(username):
    try:
        # ... follow user logic
        return True
    except Exception as e:
        print("Error: Line 155 callTwitter", e)

# Function to retrieve rules
def get_rules(id=None):
    try:
        # ... get rules logic
    except Exception as e:
        print("Error: Line 171 callTwitter", e)

# Function to delete a rule
def delete_rule(id):
    try:
        # ... delete rule logic
    except Exception as e:
        print("Error: Line 179 callTwitter", e)
