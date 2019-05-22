from django.contrib import admin
from twtscopy.models import Tweets,City,HashTags


class AdminCity(admin.ModelAdmin):
    list_display = ['id','name','latitude','longitude','range','time','active','q']
    search_fields = ('name',)


class AdminTweets(admin.ModelAdmin):
    list_display = ['city','text','searchKey','time']
    search_fields = ('text',)
    list_filter = ('city','time','searchKey')


class AdminHashTags(admin.ModelAdmin):
    def tagCity(self,obj):
         return obj.tweet.city

    def tagText(self,obj):
         return obj.tweet.text

    list_display = ['id','hashtag','time','tagCity','tagText']
    search_fields = ('hashtag',)
    list_filter = ('time','hashtag',)


admin.site.register(City,AdminCity)
admin.site.register(Tweets,AdminTweets)
admin.site.register(HashTags,AdminHashTags)
