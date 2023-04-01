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
    try:
        tweets = models.get_tweet_by_range(start,end)
        
        for tweet in tweets:
            
            try:
                name = tweet.user.user_name
                
                formatted_time = tweet.time.strftime("%I:%M %p %d/%m/%Y")
                mytweet = [name,tweet.text,tweet.link,formatted_time,tweet.id]
                text =""
            except Exception as e:
                print("Error Line 31 views ", e)
            try:
                tokens = models.get_token_by_tweet_id(tweet.id)
                
                for token in tokens:
                    text+=f"{token.token}:{token.sentiment}<br />"

                mytweet.append(text)
            except:
                pass
            
            data.append(mytweet)
    
        
        return JsonResponse({
            "actions":data
        })

    except Exception as e:
        print("Error: Line 50 views",e)
        
        return JsonResponse({
            "actions":""
        })
        
# dfgh

# This is to be used in a separate app
# This function sends a message to a specific group, identified by the ROOM_GROUP_NAME environment variable. It uses the async_to_sync function to send the message asynchronously through the channel layer, and sends a message of type "chat_message" with the provided message. This function can be used in views or other synchronous parts of the code to send messages to a group of connected websocket clients.
# def send_message_to_group(message):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(os.getenv("ROOM_GROUP_NAME"), {"type": "chat_message", "message": message})

# send_message_to_group(["wertgvc","wertg","qazxw","poiuiolk"])
