import codecs
import csv
import json
import re
import tweepy
import tweepy.cursor
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from credential import consumer_key, consumer_secret, access_token, access_secret

auth = tweepy.OAuthHandler(consumer_key,
                           consumer_secret)
auth.set_access_token(access_token,
                      access_secret)

api = tweepy.API(auth, proxy="127.0.0.1:8118")  # HTTP代理

# user = api.get_user(id='ManUtd')

# print user.screen_names


def get_tweet():
    rs_list = []
    # writer = csv.writer(codecs.open('tweepy_result_washed_already_part_2.csv', 'w', 'utf-8'))
    # writer.writerow(['text', 'likes', 'time'])
    id_placer = None
    for status in tweepy.Cursor(api.user_timeline, id='ManUtd', max_id=835956133890183168).pages():
        tweet_array = []
        favorited_count = status.favorite_count
        if favorited_count >= 1000:
            text = str(status.text)
            id_placer = status.id
            neat = re.sub(r'http.*|[\r\n\t]', '', text)
            tweet_array.append(neat)
            tweet_array.append(status.favorite_count)
            tweet_array.append(status.created_at)
            print neat
            print str(status.created_at)
            print status.favorite_count
            rs_list.append(tweet_array)
            # writer.writerow(tweet_array)
        else:
            continue
    print id_placer  # for max_id
    return rs_list


def store_data(data):
    writer = csv.writer(codecs.open('tweepy_result_washed_already_2', 'w', 'utf-8'))
    writer.writerow(['text', 'likes', 'time'])
    for item in data:
        writer.writerow(item)
    pass


def main():
    data = get_tweet()
    store_data(data)

main()


835956133890183168