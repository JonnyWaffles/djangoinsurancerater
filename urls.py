from django.conf.urls import url

from . import views
from views import AccountCreateView, AccountDetailView

app_name = 'insurancerater'
urlpatterns = [  
    url(r'^$', AccountCreateView.as_view(), name='account-create-view'),
    url(r'^accounts/(?P<pk>[0-9])/$', AccountDetailView.as_view(), name='account-detail'),
]