from django.http import HttpResponse
import itertools
import json
import datetime
from nltk.corpus import stopwords


def get_word_freq(text,sp=" ",removeStopWords=False):
    wf = {}
    stop_words = list(stopwords.words('english'))
    stop_words.append('amp')
    stop_words.append('like')
    stop_words.append('more')
    stop_words.append('know')
    stop_words.append('goes')
    for txt in text:
        txt = txt.lower()
        if removeStopWords:
            for word in txt.split(sp):
                wrd = word.strip('#&|!@#$%^&*()_+[]{};,.-')
                if not wrd in stop_words:
                    if wrd:
                        wf[wrd]=wf.get(wrd,0)+1

        else:
            for word in txt.split(sp):
                wrd = word.strip()
                wf[wrd]=wf.get(wrd,0)+1
    return wf

def myconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()

def JsonResponse(data,status=200,code=1,message="OK"): # code [0,1]
	rdata = {"status":status,"code":code,"message":message,"data":data}
	return HttpResponse(json.dumps(rdata,default=myconverter), content_type="application/json",status=status)
