from django.db import models
import datetime




class User(models.Model):

    user_name = models.CharField(max_length=200)
    author_id = models.BigIntegerField()

class Rule(models.Model):

    rule_id = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)

class Tweet(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    text = models.TextField()
    link = models.URLField()
    time = models.DateTimeField()
    tweet_id = models.BigIntegerField()

    def save(self, *args, **kwargs):
        time_str = self.time
        self.time = datetime.datetime.strptime(time_str, '%I:%M %p %d/%m/%Y')
        super().save(*args, **kwargs)


    def __str__(self):
        return self.text

class Token(models.Model):
    token = models.CharField(max_length=200)
    sentiment = models.CharField(max_length=200)
    time = models.DateTimeField()
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)



def create_tweet(tweet_arr):

    try:
        my_user = get_User_by_name(tweet_arr[0])
        tweet = Tweet(user=my_user, text=tweet_arr[1], link=tweet_arr[2], time=tweet_arr[3], tweet_id=tweet_arr[4])
        tweet.save()
    except Exception as e:
        print("Error: line 49 models",e)
        return False
    

def delete_tweet_by_id(id):
    try:
        tweet = Tweet.objects.get(id=id)
        tweet.delete()
        
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

def get_tweet_by_id(id):
    try:
        tweet = Tweet.objects.get(id=id)
        return tweet
    except Tweet.DoesNotExist:
        print("No tweets found within the specified ID.")
        return False


def get_tweet_by_range(start_id, end_id):
    
    if start_id == 0 and end_id ==0:

        try:
            last_tweet = Tweet.objects.latest('id')
            last_id = last_tweet.id

            tweets = Tweet.objects.filter(id__range=(last_id-10, last_id))
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




def create_token(token_name, sentiment, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    new_token = Token(token=token_name, sentiment=sentiment, time=tweet.time, tweet=tweet)
    new_token.save()


def get_token_by_tweet_id(tweet_id):
    tweet = get_tweet_by_id(tweet_id)
    try:
        return Token.objects.filter(tweet=tweet)
    except Token.DoesNotExist:
        return None

def create_User(user_name, author_id):
    user = get_User_by_id(author_id)
    if user is None:
        user = User(user_name=user_name, author_id=author_id)
        user.save()

def delete_User_by_name(user_name):
    try:
        user = User.objects.get(user_name=user_name)
        user.delete()
        return True
    except User.DoesNotExist:
        return False

def get_User_by_name(user_name):
    try:
        return User.objects.get(user_name=user_name)
    except User.DoesNotExist:
        return None

def get_User_by_id(author_id):
    try:
        return User.objects.get(author_id=author_id)
    except User.DoesNotExist:
        return None

def create_Rule(rule_id, user_name):
    try:
        user = get_User_by_name(user_name)
        rule = Rule(rule_id=rule_id, user=user)
        rule.save()
    except Exception as e:
        print("Error: Line 148 models",e)

def delete_Rule_by_id(rule_id):
    try:
        rule = Rule.objects.get(rule_id=rule_id)
        rule.delete()
        return True
    except Rule.DoesNotExist:
        return False

def get_Rule_by_id(rule_id):
    try:
        return Rule.objects.get(rule_id=rule_id)
    except Rule.DoesNotExist:
        return None

def get_rule_by_user(user_name):
    try:
        user = get_User_by_name(user_name)
        rule_id = Rule.objects.get(user=user).rule_id
        return rule_id
    except Exception as e:
        print("Error: line 170 models",e)

# tweet = Tweet(user='meer_barznji',text="If you love crypto workshops, we've got the perfect lineup for you 🤝 Join us in our series of workshops taking place across the MENA region, featuring an immersive and interactive experience to help you boost your Web3 knowledge. Secure your tickets now ⤵️",link='https://twitter.com/meer_barznji/status/1621560470674055169',time='08:25 PM 03/02/2023',tweet_id='1621560470674055169')
# ["meer_barznji","If you love crypto workshops, we've got the perfect lineup for you 🤝 Join us in our series of workshops taking place across the MENA region, featuring an immersive and interactive experience to help you boost your Web3 knowledge. Secure your tickets now ⤵️","https://twitter.com/meer_barznji/status/1621560470674055169","08:25 PM 03/02/2023","1621560470674055169"]