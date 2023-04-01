import os
import openai
import json
from database_manager import models

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

openai.api_key = os.getenv("OPENAI_API_KEY")

class TweetAnalyzer:

  def __init__(self,tweet):
    self.tweet_id = tweet
    tweet = models.get_tweet_by_id(tweet)
    tweet = tweet.text
    for char in ["'", '"', '/']:
        tweet = tweet.replace(char, '')

    self.tweet = tweet

  def analyze(self):
    i=0
    while i<2:
    
      try:
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=f"Please perform sentiment analysis on this tweet, and return the sentiment towards the crypto token or tokens mentioned in the tweet, in this format{{\"token\":\"sentiment\"}}. Return false if no crypto is mentioned. The tweet is: `{self.tweet}`",
          temperature=0.85,
          max_tokens=400,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        if response.choices[0].text == 'false':
          i+=1
          continue

        self.save_and_send(response.choices[0].text)
        return True
      except Exception as e:
        print(e)
        return False

  def save_and_send(self,response):
    text_to_send=""
    array_to_send = ["",""]
    try:
      json_response = json.loads(response)
      for key, value in json_response.items():
        models.create_token(key,value,self.tweet_id)
        
      
    except Exception as e:
      print("Error Line 56 analyze_tweet",e)

    try:
      tokens = models.get_token_by_tweet_id(self.tweet_id)
      for token in tokens:
        text_to_send+=f"{token.token}:{token.sentiment}<br />"

      array_to_send[0] = text_to_send
      array_to_send[1] = self.tweet_id
    except Exception as e:
      print(e)

    try:
      channel_layer = get_channel_layer()
      async_to_sync(channel_layer.group_send)(os.getenv("ROOM_GROUP_NAME"), {"type": "sentiment", "message": array_to_send})
      
    except Exception as e:
      print(e)



# $GNS at $7 and $210M Mcap is undervalued still. Stakers get about 34% of all fees, which was the equivalent of 229k last week alone. On top traders lost 825k. That $825k goes to the overcollateralization layer, designed to keep the vault protocol healthy
