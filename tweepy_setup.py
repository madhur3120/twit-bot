import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
def get_user_id(name):
    id = ""
    err = ""
    try:
        id = client.get_user(username=name).data.id  
    except Exception as e:
        print("id not found")
        err=e
    return id, err

def recent_tweets(id):
    print(type(client.get_users_tweets(id).data))
    for tweet in client.get_users_tweets(id).data:
        print(tweet.text)

def last_tweet(id):
    data=""
    for tweet in client.get_users_tweets(id).data:
        data=tweet.text
        break
    return data

def likes_count(id):
    count = 0
    tweet_count = 0
    for tweet in client.get_users_tweets(id).data:
        try:
            li =  client.get_liking_users(tweet.id).data
            for d in li:
                count+=1
        except Exception as e:
            print("err", e)
        print()
        tweet_count+=1
        if tweet_count==10:
            break
    return count

def get_user_liked(id1, id2, content):
    count = 0
    tweet_count = 0
    print(id)
    for tweet in client.get_users_tweets(id2).data:
        exists = False
        if tweet.text == content:
            exists = True
            try:
                li =  client.get_liking_users(tweet.id).data
                for d in li:
                    print(d)
                    print(d["id"])
                    if d["id"]==id1:
                        return True, tweet.id, exists;
            except Exception as e:
                return False, None, True
            print()
    return False, None, exists


def get_followers(twitterId):
    followers = 0
    err= "",
    try:
        data = client.get_users_followers(twitterId).data
        followers = data
    except Exception as e:
        print("err", e)
        err=e
    return followers, err

def get_following_count(twitterId):
    followers_count = 0
    err= "",
    try:
        data = client.get_users_following(twitterId).data
        following_count = len(data)
    except Exception as e:
        print("err", e)
        err=e
    return following_count, err