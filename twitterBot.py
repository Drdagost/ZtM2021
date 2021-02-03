# Practice using the Twitter API.
import tweepy
import time
import json

with open('keys.json') as json_file:
    keys = json.load(json_file)
    for key in keys['keys']:
        consumer_key = key['consumer_key']
        consumer_secret = key['consumer_secret']
        access_token = key['access_token']
        access_token_secret = key['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print(user.name)  # prints your name.
print(user.screen_name)
print(user.followers_count)

search = "zerotomastery"
numberOfTweets = 2


def limit_handler(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError as r:
            time.sleep(1000)
        except StopIteration:
            return


# Be nice to your followers. Follow everyone
for follower in limit_handler(tweepy.Cursor(api.followers).items()):
    print(follower.name)
    try:
        follower.follow()
        print(f'Followed {follower.name}')
    except tweepy.TweepError as e:
        print(e.reason)


# Be a narcisist and love your own tweets. or retweet anything with a keyword!
for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
    try:
        tweet.favorite()
        print('Retweeted the tweet')
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
    