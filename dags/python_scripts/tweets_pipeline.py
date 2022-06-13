import tweepy
import datetime
import pycountry
import re
import json
from kafka import KafkaProducer
import python_scripts.credentials_twitter as ct

def findcountry(text):
    for country in pycountry.countries:
        if country.alpha_2 in text or country.alpha_3 in text or country.name in text:
            # print("inside findcountry: ", text, "returning: ", country.name)
            return country.name
    # print("returning original location: ", text)


def clean_tweet(tweet):
    # Utility function to clean tweet text by removing links, special characters using simple regex statements.
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def insert_tweets():
    # I M P O R T A N T   N O T E ! ! !
    # If this script is inside Airflow, use bootstrap_servers='kafka:9092' (container_name:port) as both the Python
    # client and kafka broker are inside the same docker network. Else, use 'localhost:19092' when running this
    # script directly from the host machine as now the Python client is outside the Docker network.
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'], acks='all')
    auth = tweepy.OAuthHandler(ct.consumer_key, ct.consumer_secret)
    auth.set_access_token(ct.access_token, ct.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tweets_list = tweepy.Cursor(api.search_tweets, q="#Covid-19 since:" + str(yesterday) + " until:" + str(today),
                                tweet_mode='extended', lang='en').items()
    # add the limit (no of docs) inside items(100)

    for tweet in tweets_list:
        tweet_id = tweet.id
        text = tweet._json["full_text"]
        created_at = tweet.created_at
        location = tweet.user.location

        country = findcountry(location)
        if country is None:
            continue

        tweet_msg = clean_tweet(text)

        # dict = {'id': tweet_id, 'created_at': str(created_at), 'country': country, 'cleaned_text': new_text}
        # producer.send("covid", json.dumps(dict).encode('utf-8'))

        # FOR DISSECT PLUGIN USING , AS DELIMITER (also update logstash filter)
        message = str(tweet_id) + ',' + country + ',' + str(created_at.strftime('%Y-%m-%d')) + ',' + tweet_msg

        print(message)

        producer.send("covid", bytes(json.dumps(message), 'utf-8')).get(timeout=10)
