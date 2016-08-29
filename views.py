from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic.detail import DetailView 
from django.views.generic import View
from django.http import HttpResponseRedirect
from models import AccountInfo, Quote, RiskData
from .forms import AccountInfoForm, RiskDataForm, InsuringAgreementForm

# Create your views here.

class AccountCreateView(CreateView):
  model = AccountInfo
  fields = ['name', 'underwriter', 'rating_state', 'entity_type']
  template_name = "djangoinsurancerater/accountinfo_form.html" 
  
class AccountUpdateView(UpdateView):
  model = AccountInfo
  fields = ['name', 'underwriter', 'rating_state', 'entity_type']
  template_name = "djangoinsurancerater/accountinfo_form.html"

class QuoteView(View):
  def get(self, request, *args, **kwargs):
    accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
    accountinfoform = AccountInfoForm(instance=accountinfo)
    riskdataform = RiskDataForm()
    context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform}
    return render(request, 'djangoinsurancerater/quotes.html', context)
    
    
    
    

      