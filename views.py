from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView 
from django.views.generic import View
from django.forms import inlineformset_factory, formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from models import AccountInfo, Quote, RiskData, ClassCode, InsuringAgreement, AgreementType
from .forms import AccountInfoForm, RiskDataForm, InsuringAgreementForm, ClassCodeSelectForm
import operator
# Create your views here.

class AccountCreateView(View):
  def get(self, request, *args, **kwargs):
    #I need a search box that queries all the account names, search results are shown below. AccountInform form with a new button that posts an
    #account to the DB and returns the AccountUpdateView.
    newaccountform = AccountInfoForm()
    lastfiveaccounts = AccountInfo.objects.all().order_by('-date')[:5]
    context = {'accountinfoform' : newaccountform, 'lastfiveaccounts' : lastfiveaccounts}
    return render(request, 'djangoinsurancerater/home.html', context)
  
  def post(self, request, *args, **kwargs):
    newaccountform = AccountInfoForm(request.POST)
    lastfiveaccounts = AccountInfo.objects.all().order_by('-date')[:5]
    context = {'accountinfoform' : newaccountform, 'lastfiveaccounts' : lastfiveaccounts}
    if newaccountform.is_valid():
      newaccount = newaccountform.save()
      return redirect(newaccount)
    else:
      return render(request, 'djangoinsurancerater/home.html', context)    
  
class AccountUpdateView(View):
  def get(self, request, *args, **kwargs):
    account = get_object_or_404(AccountInfo, pk=kwargs['pk'])
    accountinfoform = AccountInfoForm(instance=account)
    lastfivequotes = account.quotes.all().order_by('-created_time')[:5]
    context = {'accountinfoform' : accountinfoform, 'lastfivequotes' : lastfivequotes}
    return render(request, 'djangoinsurancerater/accountinfo.html', context)

class AccountSearchListView(ListView):
  model = AccountInfo
  paginate_by = 10
  
  def get_queryset(self):
    result = super(AccountSearchListView, self).get_queryset()
    query = self.request.GET.get('q')
    if query:
      query_list = query.split()
      result = result.filter(reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
                            )
    return result
  
  

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
    accountinfoform = AccountInfoForm(instance = accountinfo)
    riskdataform = RiskDataForm(instance = quote.risk_data)
    print "GET CLASS CODE IS %s" % (quote.class_code)
    classcodeform = ClassCodeSelectForm(instance = quote.class_code)
    insuring_agreements = quote.agreements.all()
    insuring_agreement_forms = [ InsuringAgreementForm(instance = insuring_agreement) for insuring_agreement in insuring_agreements ]
    context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform, 'insuring_agreement_forms' : insuring_agreement_forms}
    return render(request, 'djangoinsurancerater/quote.html', context)
    
  def post(self, request, *args, **kwargs):
    accountinfo = get_object_or_404(AccountInfo, pk=kwargs['pk'])
    quote = get_object_or_404(Quote, pk=kwargs['quoteid'])
    accountinfoform = AccountInfoForm(request.POST, instance = accountinfo)
    riskdataform = RiskDataForm(request.POST, instance = quote.risk_data)
    classcodeform = ClassCodeSelectForm(request.POST, instance = quote.class_code)
    context = {'accountinfoform' : accountinfoform, 'riskdataform' : riskdataform, 'classcodeform' : classcodeform }
    if request.is_ajax():
      insuring_agreement_form = InsuringAgreementForm(request.POST, instance = quote.agreements.get
                                                      (agreement_type__exact = request.POST['agreement_type'])
                                                     )
      if insuring_agreement_form.is_valid():
        print("valid")
        insuring_agreement = insuring_agreement_form.save()
        insuring_agreement.premium = insuring_agreement.calc_agreement_premium(quote)
        insuring_agreement.save()        
        return JsonResponse({'premium' : insuring_agreement.premium })
      else:
        print(insuring_agreement_form.errors)
        return redirect(quote)

    if accountinfoform.is_valid() and riskdataform.is_valid() and classcodeform.is_valid():
      accountinfoform.save()
      riskdataform.save()
      classcode_to_query = classcodeform.cleaned_data['class_code']
      classcode = ClassCode.objects.get(class_code = classcode_to_query)
      quote.class_code = classcode
      quote.save()
      return redirect(quote)
    else:
      accountinfoform = AccountInfoForm(request.POST)
      riskdataform = RiskDataForm(request.POST)
      classcodeform = ClassCodeSelectForm(request.POST)
      return render(request, 'djangoinsurancerater/quote.html', context)

class ClassCodeSearch(ListView):
  model = ClassCode
  paginate_by = 10
  
  def get_queryset(self):
    result = super(ClassCodeSearch, self).get_queryset()
    query = self.request.GET.get('q')
    if query:
      query_list = query.split()
      result = result.filter(reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list))
                            )
    return result

      

    
    

      