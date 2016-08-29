from django.conf.urls import url

from . import views
from views import AccountCreateView, AccountUpdateView, QuoteView

app_name = 'djangoinsurancerater'
urlpatterns = [  
    url(r'^$', AccountCreateView.as_view(), name='account-create-view'),
    url(r'^accounts/(?P<pk>\d+)/$', AccountUpdateView.as_view(), name='account-detail'),
    url(r'^accounts/(?P<pk>\d+)/quotes/$', QuoteView.as_view(), name='quotes'),
]