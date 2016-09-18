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

class APIView(View):
  def get(self, request, *args, **kwargs):
    #API needs agreements, class_code, employees, limit, deductible
    #Returns premium as Json
    errors = []
    request_dict = request.GET
    #Agreements post should be single string with numbers ie. 1238 each number an agreement or "A" for All, which is default
    request_agreements = request_dict.get('agreements', 'A')
    agreement_types = []
    for character in request_agreements:
      if character == 'a' or character == 'A':        
        for agreements in AgreementType.objects.all():
          agreement_types.append(agreements)
      else:
          #Note this will only work in production when each agreement has the right ID 1-9
          agreement_types.append(AgreementType.objects.get(id = character))
    class_code = ClassCode.objects.get(class_code = request_dict.get('class_code', '635-41'))
    employees = 0
    try:
      employees = request_dict['employees']
    except KeyError as e:
      errors.append("Employee Count Must Be Provided")
      return JsonResponse({'errors': errors }, safe = False)
    limit = int(filter(lambda x: x.isdigit(), (request_dict.get('limit', '1000000'))))
    deductible = int(filter(lambda x: x.isdigit(), (request_dict.get('deductible', '10000'))))
    #limit and deductible default to $1M/$10k
    accountinfo = AccountInfo()    
    risk_data = RiskData()
    risk_data.rateable_count = employees
    quote = Quote(account_info = accountinfo, class_code = class_code, risk_data = risk_data)
    quote_insuring_agreement_list = []
    for agreement in agreement_types:      
      IA = InsuringAgreement(insurance_limit = limit, deductible = deductible, 
                                             agreement_type = agreement, quote = quote)
      quote_insuring_agreement_list.append(IA)
    premium = 0
    for insuring_agreement in quote_insuring_agreement_list:
      print "Insuring Agreement: %s   Premium:  %s" % (insuring_agreement.agreement_type, insuring_agreement.calc_agreement_premium(quote))
      premium = premium + insuring_agreement.calc_agreement_premium(quote)
    return JsonResponse({'premium' : round(premium, 2)})
 
      
    

    
    

      