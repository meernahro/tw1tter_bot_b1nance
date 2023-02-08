from django.shortcuts import render
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os
import asyncio
from database_manager import models

def index(request):
    return render(request,"twitter/index.html")
    

def actions(request):
    
    # Get start and end points
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or 0)
    data = []

    tweets = models.get_tweet_by_range(start,end)
    for tweet in tweets:
        print(tweet.id)
        mytweet = [tweet.user,tweet.text,tweet.link,tweet.time,tweet.id]
        data.append(mytweet)
        


    return JsonResponse({
        "actions":data
    })



# This is to be used in a separate app
# This function sends a message to a specific group, identified by the ROOM_GROUP_NAME environment variable. It uses the async_to_sync function to send the message asynchronously through the channel layer, and sends a message of type "chat_message" with the provided message. This function can be used in views or other synchronous parts of the code to send messages to a group of connected websocket clients.
# def send_message_to_group(message):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(os.getenv("ROOM_GROUP_NAME"), {"type": "chat_message", "message": message})

# send_message_to_group(["wertgvc","wertg","qazxw","poiuiolk"])
