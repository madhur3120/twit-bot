import tweepy

api_key = "IuMVrLtepL3WBMiReobjXmlsh"
api_secret = "w24tlUcCLjfwiTVXm4gaGTSq6PcnJwugOywSnnQumtXQJabPT5"
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAMGojQEAAAAAepVhSxL0s4kR3UqoZXPrrKCNSaA%3Dgt2eISsj71V8F1TuCHiTepEpAskZJKVJsMBSMO3j4YFLZY7w3z"
access_token = "811458373430296576-zFTGn8CfFLNTOftWiEb04aaOx5meLHu"
access_token_secret = "veNegEnEYwTr5ywTkDKwS1F33JaP4pGv1THxdqiqInHAh"

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
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

def get_followers_count(twitterId):
    followers_count = 0
    err= "",
    try:
        data = client.get_users_followers(twitterId).data
        followers_count = len(data)
    except Exception as e:
        print("err", e)
        err=e
    return followers_count, err

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