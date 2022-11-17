import tweepy

api_key = "IuMVrLtepL3WBMiReobjXmlsh"
api_secret = "w24tlUcCLjfwiTVXm4gaGTSq6PcnJwugOywSnnQumtXQJabPT5"
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAMGojQEAAAAAepVhSxL0s4kR3UqoZXPrrKCNSaA%3Dgt2eISsj71V8F1TuCHiTepEpAskZJKVJsMBSMO3j4YFLZY7w3z"
access_token = "811458373430296576-zFTGn8CfFLNTOftWiEb04aaOx5meLHu"
access_token_secret = "veNegEnEYwTr5ywTkDKwS1F33JaP4pGv1THxdqiqInHAh"

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# for tweet in api.home_timeline():
#     print(tweet.text)

person = client.get_user(username="madhursaxena_").data.id

def get_user_id(name):
    return client.get_user(username=name).data.id

def recent_tweets(id):
    print(type(client.get_users_tweets(id).data))
    for tweet in client.get_users_tweets(id).data:
        print(tweet.text)
# for tweet in client.get_users_tweets(person).data:
#     print(tweet.text)
def last_tweet(id):
    data=""
    for tweet in client.get_users_tweets(id).data:
        data=tweet.text
        print(tweet.id)
        break
    return data

def likes_count(id):
    for tweet in client.get_users_tweets(id).data:
        try:
            for d in client.get_liking_users(tweet.id).data:
                print(d.name)
        except:
            print(tweet.id,"no likes")
        # print(tw)
        print()
        


