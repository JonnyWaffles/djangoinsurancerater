from django.conf.urls import url

from . import views
from views import AccountCreateView, AccountUpdateView, QuoteCreateView, QuoteUpdateView, AccountSearchListView, ClassCodeSearch, APIView

app_name = 'djangoinsurancerater'
urlpatterns = [  
    url(r'^$', AccountCreateView.as_view(), name='account-create-view'),
    url(r'^codes/$', ClassCodeSearch.as_view(), name='class-code-search-view'),
    url(r'^api/$', APIView.as_view(), name='api-view'),
    url(r'^accounts/search/$', AccountSearchListView.as_view(), name='account-search-list-view'),
    url(r'^accounts/(?P<pk>\d+)/$', AccountUpdateView.as_view(), name='account-update-view'),
    url(r'^accounts/(?P<pk>\d+)/quote/$', QuoteCreateView.as_view(), name='quote-create-view'),
    url(r'^accounts/(?P<pk>\d+)/quote/(?P<quoteid>\d+)$', QuoteUpdateView.as_view(), name='quote-update-view')
]