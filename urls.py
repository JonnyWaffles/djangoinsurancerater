from django.conf.urls import url

from . import views
from views import AccountCreateView, AccountUpdateView, QuoteCreateView, QuoteUpdateView

app_name = 'djangoinsurancerater'
urlpatterns = [  
    url(r'^$', AccountCreateView.as_view(), name='account-create-view'),
    url(r'^accounts/(?P<pk>\d+)/$', AccountUpdateView.as_view(), name='account-detail'),
    url(r'^accounts/(?P<pk>\d+)/quote/$', QuoteCreateView.as_view(), name='quote-create-view'),
    url(r'^accounts/(?P<pk>\d+)/quote/(?P<quoteid>\d+)$', QuoteUpdateView.as_view(), name='quote-detail')
]