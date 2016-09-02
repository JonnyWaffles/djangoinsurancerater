from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic.detail import DetailView 
from django.views.generic import View
from django.forms import inlineformset_factory, formset_factory
from django.http import HttpResponseRedirect
from models import AccountInfo, Quote, RiskData, ClassCode, InsuringAgreement, AgreementType
from .forms import AccountInfoForm, RiskDataForm, InsuringAgreementForm, ClassCodeSelectForm

# Create your views here.

class AccountCreateView(CreateView):
  model = AccountInfo
  fields = ['name', 'underwriter', 'rating_state', 'entity_type']
  template_name = "djangoinsurancerater/accountinfo_form.html" 
  
class AccountUpdateView(UpdateView):
  model = AccountInfo
  fields = ['name', 'underwriter', 'rating_state', 'entity_type']
  template_name = "djangoinsurancerater/accountinfo_form.html"

class QuoteCreateView(View):
  def get(self, request, *args, **kwargs):
    accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
    accountinfoform = AccountInfoForm(instance=accountinfo)
    riskdataform = RiskDataForm()
    classcodeform = ClassCodeSelectForm()
    context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform}
    return render(request, 'djangoinsurancerater/quote.html', context)
  
  ##Need to write a post that generates a Quote with RiskData and directs to QuoteUpdateView with the appropriate quoteid as an argument
  def post(self, request, *args, **kwargs):
    accountinfoform = AccountInfoForm(request.POST, instance = get_object_or_404(AccountInfo, pk=kwargs['pk']))
    riskdataform = RiskDataForm(request.POST)
    classcodeform = ClassCodeSelectForm(request.POST, instance = get_object_or_404(ClassCode, pk=request.POST['class_code']))
    
    if accountinfoform.is_valid() and riskdataform.is_valid() and classcodeform.is_valid():
      accountinfo = accountinfoform.save()
      classcode_to_query = classcodeform.cleaned_data['class_code']
      classcode = ClassCode.objects.get(class_code = classcode_to_query)
      riskdata = riskdataform.save()
      quote = Quote(account_info = accountinfoform.instance, risk_data = riskdata, class_code = classcode)
            ##Add the 9 agreements to the quote object
      agreementtypes = AgreementType.objects.all()
      quote.save()
      for agreement in agreementtypes:
        quote.agreements.add(InsuringAgreement(agreement_type = agreement), bulk=False)      
      return redirect(quote)
    
    else:
      accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
      accountinfoform = AccountInfoForm(instance=accountinfo)
      riskdataform = RiskDataForm(request.POST)
      classcodeform = ClassCodeSelectForm(request.POST)
      context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform}
      return render(request, 'djangoinsurancerater/quote.html', context)
  
class QuoteUpdateView(View):
  def get(self, request, *args, **kwargs):
      accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
      quote = get_object_or_404(Quote, pk=kwargs['quoteid'])
      accountinfoform = AccountInfoForm(instance=accountinfo)
      riskdataform = RiskDataForm(instance = quote.risk_data)
      classcodeform = ClassCodeSelectForm(instance = quote.class_code)
      InsuringAgreementFormSet = inlineformset_factory(Quote, InsuringAgreement, fields = ('insurance_limit', 'deductible', 'premium'), extra = 0)
      insuringagreementforms = InsuringAgreementFormSet(instance = quote)      
      context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform, 'insuringagreementforms' : insuringagreementforms}
      return render(request, 'djangoinsurancerater/quote.html', context)
    
  def post(self, request, *args, **kwargs):
      accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
      quote = get_object_or_404(Quote, pk=kwargs['quoteid'])
      accountinfoform = AccountInfoForm(request.POST, instance=accountinfo)
      riskdataform = RiskDataForm(request.POST, instance = quote.risk_data)
      classcodeform = ClassCodeSelectForm(request.POST, instance = quote.class_code)
      InsuringAgreementFormSet = inlineformset_factory(Quote, InsuringAgreement)
      insuringagreementforms = InsuringAgreementFormSet(request.POST, instance = quote, fields = ('insurance_limit', 'deductible', 'premium'))  
      context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform, 'insuringagreementforms' : insuringagreementforms}
      if accountinfoform.is_valid() and riskdataform.is_valid() and classcodeform.is_valid() and insuringagreementforms.is_valid():
        accountinfoform.save()
        riskdataform.save()
        classcodeform.save()
        insuringagreementforms.save()
        return redirect(quote)
    
    

    
    

      