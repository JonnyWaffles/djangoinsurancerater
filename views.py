from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic.detail import DetailView 
from django.http import HttpResponseRedirect
from models import AccountInfo, Quote

# Create your views here.

class AccountCreateView(CreateView):
  model = AccountInfo
  fields = ['name', 'rating_state', 'entity_type']
  template_name = "djangoinsurancerater/accountinfo_form.html" 
  
class AccountDetailView(UpdateView):
  model = AccountInfo
  fields = ['name', 'rating_state', 'entity_type']
  template_name ="djangoinsurancerater/accountinfo_form.html"

class QuoteCreateView(CreateView):
  model = Quote
  fields = ['underwriter', 'created_time']

      