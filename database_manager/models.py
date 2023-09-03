from django.db import models
import datetime


class User(models.Model):
    """
    Represents a user with a username and author ID.
    """
    user_name = models.CharField(max_length=200)
    author_id = models.BigIntegerField()

    def __str__(self):
        return self.user_name


class Rule(models.Model):
    """
    Represents a rule with an ID and a reference to a user.
    """
    rule_id = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.rule_id)


class Tweet(models.Model):
    """
    Represents a tweet with user reference, text content, link, timestamp, and tweet ID.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    link = models.URLField()
    time = models.DateTimeField()
    tweet_id = models.BigIntegerField()

    def save(self, *args, **kwargs):
        """
        Overriding the save method to convert time string to datetime before saving.
        """
        time_str = self.time
        self.time = datetime.datetime.strptime(time_str, '%I:%M %p %d/%m/%Y')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text


class Token(models.Model):
    """
    Represents a token with its sentiment, timestamp and associated tweet.
    """
    token = models.CharField(max_length=200)
    sentiment = models.CharField(max_length=200)
    time = models.DateTimeField()
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.token


def create_tweet(tweet_arr):
    """
    Creates a tweet using an array of values.
    Args:
    - tweet_arr: List containing [user_name, text, link, time, tweet_id]
    """
    try:
        my_user = get_User_by_name(tweet_arr[0])
        tweet = Tweet(user=my_user, text=tweet_arr[1], link=tweet_arr[2], time=tweet_arr[3], tweet_id=tweet_arr[4])
        tweet.save()
    except Exception as e:
        print(f"Error while creating tweet: {e}")
        return False


def delete_tweet_by_id(id):
    """
    Deletes a tweet by its ID.
    Args:
    - id: Tweet's ID to delete.
    """
    try:
        tweet = Tweet.objects.get(id=id)
        tweet.delete()
        return True
    except Tweet.DoesNotExist:
        return False


def get_tweet_by_tweet_id(tweet_id):
    """
    Retrieves a tweet by its tweet ID.
    Args:
    - tweet_id: ID of the tweet to retrieve.
    """
    try:
        return Tweet.objects.get(tweet_id=tweet_id)
    except Tweet.DoesNotExist:
        print("No tweets found with the specified ID.")
        return False


def get_tweet_by_id(id):
    """
    Retrieves a tweet by its database ID.
    Args:
    - id: Database ID of the tweet to retrieve.
    """
    try:
        return Tweet.objects.get(id=id)
    except Tweet.DoesNotExist:
        print("No tweets found with the specified ID.")
        return False


def get_tweet_by_range(start_id, end_id):
    """
    Retrieves tweets in a given range of IDs.
    Args:
    - start_id: Start of the ID range.
    - end_id: End of the ID range.
    """
    try:
        return Tweet.objects.filter(id__range=(start_id, end_id)).order_by('-id')
    except Tweet.DoesNotExist:
        print("No tweets found within the specified ID range.")
        return False


def create_token(token_name, sentiment, tweet_id):
    """
    Creates a token associated with a tweet.
    Args:
    - token_name: Name of the token.
    - sentiment: Sentiment value of the token.
    - tweet_id: ID of the associated tweet.
    """
    tweet = Tweet.objects.get(id=tweet_id)
    new_token = Token(token=token_name, sentiment=sentiment, time=tweet.time, tweet=tweet)
    new_token.save()


def get_token_by_tweet_id(tweet_id):
    """
    Retrieves tokens associated with a given tweet ID.
    Args:
    - tweet_id: ID of the tweet for which tokens are to be retrieved.
    """
    tweet = get_tweet_by_id(tweet_id)
    try:
        return Token.objects.filter(tweet=tweet)
    except Token.DoesNotExist:
        return None


def create_User(user_name, author_id):
    """
    Creates a user with a given username and author ID.
    Args:
    - user_name: Name of the user.
    - author_id: Author ID of the user.
    """
    user = get_User_by_id(author_id)
    if user is None:
        user = User(user_name=user_name, author_id=author_id)
        user.save()


def delete_User_by_name(user_name):
    """
    Deletes a user by their username.
    Args:
    - user_name: Name of the user to delete.
    """
    try:
        user = User.objects.get(user_name=user_name)
        user.delete()
        return True
    except User.DoesNotExist:
        return False


def get_User_by_name(user_name):
    """
    Retrieves a user by their username.
    Args:
    - user_name: Name of the user to retrieve.
    """
    try:
        return User.objects.get(user_name=user_name)
    except User.DoesNotExist:
        return None


def get_User_by_id(author_id):
    """
    Retrieves a user by their author ID.
    Args:
    - author_id: Author ID of the user to retrieve.
    """
    try:
        return User.objects.get(author_id=author_id)
    except User.DoesNotExist:
        return None


def create_Rule(rule_id, user_name):
    """
    Creates a rule with a given rule ID and user name.
    Args:
    - rule_id: ID of the rule.
    - user_name: Name of the user associated with the rule.
    """
    try:
        user = get_User_by_name(user_name)
        rule = Rule(rule_id=rule_id, user=user)
        rule.save()
    except Exception as e:
        print(f"Error while creating rule: {e}")


def delete_Rule_by_id(rule_id):
    """
    Deletes a rule by its rule ID.
    Args:
    - rule_id: ID of the rule to delete.
    """
    try:
        rule = Rule.objects.get(rule_id=rule_id)
        rule.delete()
        return True
    except Rule.DoesNotExist:
        return False


def get_Rule_by_id(rule_id):
    """
    Retrieves a rule by its rule ID.
    Args:
    - rule_id: ID of the rule to retrieve.
    """
    try:
        return Rule.objects.get(rule_id=rule_id)
    except Rule.DoesNotExist:
        return None


def get_rule_by_user(user_name):
    """
    Retrieves the rule ID associated with a given user name.
    Args:
    - user_name: Name of the user for which the rule ID is to be retrieved.
    """
    try:
        user = get_User_by_name(user_name)
        rule_id = Rule.objects.get(user=user).rule_id
        return rule_id
    except Exception as e:
        print(f"Error while fetching rule by user: {e}")


# Sample data
# tweet = Tweet(user='meer_barznji',text="If you love crypto workshops, we've got the perfect lineup for you 🤝 Join us in our series of workshops taking place across the MENA region, featuring an immersive and interactive experience to help you boost your Web3 knowledge. Secure your tickets now ⤵️",link='https://twitter.com/meer_barznji/status/1621560470674055169',time='08:25 PM 03/02/2023',tweet_id='1621560470674055169')
