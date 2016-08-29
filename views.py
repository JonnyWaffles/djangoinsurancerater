from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic.detail import DetailView 
from django.http import HttpResponseRedirect
from models import AccountInfo, Quote, RiskData 

# Create your views here.

class AccountCreateView(CreateView):
  model = AccountInfo
  fields = ['name', 'underwriter', 'rating_state', 'entity_type']
  template_name = "djangoinsurancerater/accountinfo_form.html" 
  
class AccountUpdateView(UpdateView):
  model = AccountInfo
  fields = ['name', 'underwriter', 'rating_state', 'entity_type']
  template_name = "djangoinsurancerater/accountinfo_form.html"

""" Psuedo Code Time

class QuoteCreateView(CreateView):
  model = Quote
  fields = ['underwriter', 'created_time', 'account_info']

"""

      