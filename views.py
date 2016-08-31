from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic.detail import DetailView 
from django.views.generic import View
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from models import AccountInfo, Quote, RiskData, ClassCode, InsuringAgreement 
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
      quote.save()
      return redirect(quote)
    else:
      accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
      accountinfoform = AccountInfoForm(instance=accountinfo)
      riskdataform = RiskDataForm()
      classcodeform = ClassCodeSelectForm()
      context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform}
      return render(request, 'djangoinsurancerater/quote.html', context)
  
class QuoteUpdateView(View):    
    def get(self, request, *args, **kwargs):
      accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
      quote = get_object_or_404(Quote, pk=kwargs['quoteid'])
      accountinfoform = AccountInfoForm(instance=accountinfo)
      riskdataform = RiskDataForm(instance = quote.risk_data)
      classcodeform = ClassCodeSelectForm(instance = quote.class_code)
      ## We need to set up 9 Empty forms, one for each AgreementType
      ## Set each one's agreement_type field to a different AgreementType objects
      ## Then set the InsuringAgreement forms to any insuring_agreements objects that exist in quote.agreements.all()
      initialagreementforms = modelformset_factory(InsuringAgreement, fields=('agreement_type', 'insurance_limit', 'deductible', 'premium'))
      
      InsuringAgreementFormSet = inlineformset_factory(Quote, InsuringAgreement, fields=('agreement_type', 'insurance_limit', 'deductible', 'premium'))
      InsuringAgreementForms = InsuringAgreementFormSet(instance = quote)      
      context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform, 'InsuringAgreementForms' : InsuringAgreementForms}
      return render(request, 'djangoinsurancerater/quote.html', context)
    
    def post(self, request, *args, **kwargs):
      accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
      quote = get_object_or_404(Quote, pk=kwargs['quoteid'])
      accountinfoform = AccountInfoForm(request.POST, instance=accountinfo)
      riskdataform = RiskDataForm(request.POST, instance = quote.risk_data)
      classcodeform = ClassCodeSelectForm(request.POST, instance = quote.class_code)
      InsuringAgreementFormSet = inlineformset_factory(Quote, InsuringAgreement, fields=('agreement_type', 'insurance_limit', 'deductible', 'premium'))
      InsuringAgreementForms = InsuringAgreementFormSet(request.POST, instance = quote)  
      context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform, 'InsuringAgreementForms' : InsuringAgreementForms}
      if accountinfoform.is_valid() and riskdataform.is_valid() and classcodeform.is_valid() and InsuringAgreementForms.is_valid():
        accountinfoform.save()
        riskdataform.save()
        classcodeform.save()
        InsuringAgreementForms.save()
        return redirect(quote)
    
    

    
    

      