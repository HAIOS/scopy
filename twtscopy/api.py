from twtscopy.utils import JsonResponse
from twtscopy.models import HashTags,Tweets
from django.db.models import Count
from django.forms.models import model_to_dict

class TwtscopyAPI(object):
    """docstring for CluesAPI."""
    def __init__(self):
        pass

    def topHashTags(self,request):
        kargs = {'tweet__searchKey':''}
        if request.GET:
            if request.GET.get("city"):
                kargs['tweet__city__name__contains'] = request.GET.get("city")


        hashtags  = HashTags.objects.filter(**kargs).values('hashtag').annotate(dcount=Count('hashtag'))
        data = [(x["hashtag"],x["dcount"]) for x in hashtags]
        data.sort(key=lambda x :x[1],reverse=True)
        return JsonResponse(data[0:10])


    def tweets(self,request):
        kargs = {}
        if request.GET:
            if request.GET.get("city"):
                kargs['city__name__contains'] = request.GET.get("city")

            if request.GET.get("searchkey"):
                kargs['searchKey__contains'] = request.GET.get("searchkey")

        data = [model_to_dict(x) for x in Tweets.objects.filter(**kargs)[0:100]]
        return JsonResponse(data)
