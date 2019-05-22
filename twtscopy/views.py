from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import Count

from twtscopy.utils import get_word_freq
from twtscopy.models import City,Tweets,HashTags
import pandas as pd

class HaikusView:
    def __init__(self):
        pass


    def locations(self,request):
        cities = City.objects.all()
        cities  = [model_to_dict(city) for city in cities]
        df  = pd.DataFrame(cities)
        df = df[['id','name','latitude','longitude','range','q','time','active']]
        df.range = [str(range)+" Km"for range in df.range]
        table = df.to_html(index=False,border=0,classes=("table","table-hover","table-striped"))
        data ={'table':{'data':table,'title':'Scopy Locations','description':'scopy actively wathing on below cities'}}
        return render(request, 'twtscopy/locations.html', data)


    def dashboard(self,request):
        tweets = Tweets.objects.filter(searchKey='5G Ericsson')
        texts = [twt.text for twt in tweets]
        textsFreq = [x for x in get_word_freq(texts," ",True).items()]
        textsFreq.sort(key=lambda x :x[1],reverse=True)
        data = {'texts':textsFreq[0:500]}


        return render(request, 'twtscopy/dashboard.html', data)


    def tweets(self,request):
        start = 0
        end = 100
        kargs = {}
        _kargs = {}
        if request.GET:
            if request.GET.get("p"):
                p = int(request.GET.get("p"))
                start = (p-1)*100
                end = start+100-1

            if request.GET.get("city"):
                kargs['city__name__contains'] = request.GET.get("city")

        cities = City.objects.all()

        tweets = Tweets.objects.filter(**kargs)[start:end]

        data = {'nav':'tweets',"cities":cities,'tweets':tweets}

        return render(request, 'twtscopy/tweets.html', data)


    def hashtags(self,request):
        start = 0
        end = 100
        kargs = {}
        _kargs = {}
        if request.GET:
            if request.GET.get("p"):
                p = int(request.GET.get("p"))
                start = (p-1)*100
                end = start+100-1

            if request.GET.get("city"):
                _kargs['tweet__city__name__contains'] = request.GET.get("city")

        cities = City.objects.all()

        hashtags  = HashTags.objects.filter(**_kargs).values('hashtag').annotate(dcount=Count('hashtag'))
        topHashtags = [(x["hashtag"],x["dcount"]) for x in hashtags]
        topHashtags.sort(key=lambda x :x[1],reverse=True)

        data = {'nav':'dashboard','topHashtags':topHashtags}

        return render(request, 'twtscopy/hashtags.html', data)
