from django.db import models
import datetime


class Tweet(models.Model):
    
    user = models.CharField(max_length=200)
    text = models.TextField()
    link = models.URLField()
    time = models.DateTimeField()
    tweet_id = models.BigIntegerField()

    def save(self, *args, **kwargs):
        time_str = self.time
        self.time = datetime.datetime.strptime(time_str, '%I:%M %p %m/%d/%Y')
        super().save(*args, **kwargs)


    def __str__(self):
        return self.text

def create_tweet(tweet_arr):

    try:
        tweet = Tweet(user=tweet_arr[0], text=tweet_arr[1], link=tweet_arr[2], time=tweet_arr[3], tweet_id=tweet_arr[4])
        tweet.save()
    except Exception as e:
        print("Error creating tweet",e)
        return False
    

def delete_tweet_by_id(id):
    try:
        tweet = Tweet.objects.get(id=id)
        tweet.delete()
        print(id)
        return True
    except Tweet.DoesNotExist:
        return False

def get_tweet_by_tweet_id(tweet_id):
    try:
        tweet = Tweet.objects.get(tweet_id=tweet_id)
        return tweet
    except Tweet.DoesNotExist:
        print("No tweets found within the specified ID.")
        return False

def get_tweet_by_range(start_id, end_id):
    
    if start_id == 0 and end_id ==0:

        try:
            last_tweet = Tweet.objects.latest('id')
            last_id = last_tweet.id

            tweets = Tweet.objects.filter(id__range=(last_id-20, last_id))
            return tweets
        except Tweet.DoesNotExist:
            print("No tweets found within the specified ID range.")
            return False
    else:
        try:
            tweets = Tweet.objects.filter(id__range=(start_id, end_id)).order_by('-id')
            return tweets
        except Tweet.DoesNotExist:
            print("No tweets found within the specified ID range.")
            return False





# tweet = Tweet(user='meer_barznji',text="If you love crypto workshops, we've got the perfect lineup for you 🤝 Join us in our series of workshops taking place across the MENA region, featuring an immersive and interactive experience to help you boost your Web3 knowledge. Secure your tickets now ⤵️",link='https://twitter.com/meer_barznji/status/1621560470674055169',time='08:25 PM 03/02/2023',tweet_id='1621560470674055169')
["meer_barznji","If you love crypto workshops, we've got the perfect lineup for you 🤝 Join us in our series of workshops taking place across the MENA region, featuring an immersive and interactive experience to help you boost your Web3 knowledge. Secure your tickets now ⤵️","https://twitter.com/meer_barznji/status/1621560470674055169","08:25 PM 03/02/2023","1621560470674055169"]