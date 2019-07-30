from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from twtscopy.models import City,Tweets,HashTags
import time
import random
from multiprocessing import Process

#twt API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import json


def make_id():
    t = int(time.time()*1000) - 1489691362678
    u = random.SystemRandom().getrandbits(23)
    id = (t << 23 ) | u
    return int(id)


class Command(BaseCommand):
    help = 'Collecting data form tweeter API'

    def handle(self, *args, **options):
        self.TWEET_API = dict(settings.TWEET_API)
        access_token = self.TWEET_API.get("access_token")
        access_token_secret = self.TWEET_API.get("access_token_secret")
        consumer_key = self.TWEET_API.get("consumer_key")
        consumer_secret = self.TWEET_API.get("consumer_secret")
        self.FETCHLIMIT  = int(settings.FETCHLIMIT)

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth)


        # data = Cursor(api.search, q='', geocode="28.459497,77.026634,10km",tweet_mode="extended").items(1000)
        cities = City.objects.filter(active=True)
        #self.getDataForCity(cities[0])
        plist = []

        for city in cities:
            p = Process(target=self.getDataForCity, args=(city,))
            plist.append(p)

        for p in plist:
            p.start()

        for p in plist:
            p.join()


    def getDataForCity(self,city):
        if city.active:
            if city.q:
                q = str(city.q)
            else:
                q = ''

            if city.latitude and city.longitude:
                geocode = "%f,%f,%dkm" % (city.latitude,city.longitude,city.range)
                data = Cursor(self.api.search, q=q, geocode=geocode,tweet_mode="extended").items(self.FETCHLIMIT)
            else:
                data = Cursor(self.api.search, q=q,tweet_mode="extended").items(self.FETCHLIMIT)

            print(city)
            for twt in data:
                tweet = Tweets(id = make_id(),text=twt._json["full_text"],city=city,searchKey=q)
                tweet._json = json.dumps(twt._json)
                tweet.tweet_id = twt._json["id"]
                tweet.user_id = twt._json.get("user",{}).get("id")
                tweet.user_name = twt._json.get("user",{}).get("name")
                tweet.user_image = twt._json.get("user",{}).get("profile_image_url")
                tweet.save()
                print(city,"-->",tweet.text)
                time.sleep(2)
                hashtags = twt._json.get("entities").get("hashtags",[])
                if hashtags:
                    for htag in hashtags:
                        pass
                        hashtag = HashTags(id = make_id(),tweet=tweet,hashtag=htag.get("text"))
                        hashtag.save()
                else:
                    print("no hastag found")
