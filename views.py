from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from forms import AccountInfoForm
from models import AccountInfo

# Create your views here.

class AccountCreateView(CreateView):
  model = AccountInfo
  fields = ['name', 'rating_state', 'entity_type']
  template_name = "djangoinsurancerater/accountinfo_form.html"    
  
class AccountDetailView(DetailView):
  model = AccountInfo
  template_name ="djangoinsurancerater/accountinfo_detail"


      