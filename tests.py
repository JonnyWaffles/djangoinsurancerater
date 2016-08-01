from insurancerater.models import * 
from django.test import TestCase
from datetime import date
# Create your tests here.

class Quoter(TestCase):
  fixtures = ["exposureRow134.json"]
  
  def setUp(cls):
    accountinfo = AccountInfo.objects.create(name = "TestQuote", date = date(2016, 7, 18))
    riskdata = RiskData.objects.create(employee_count = 5, rateable_count = 5, locations = 1)
    classcode = ClassCode.objects.create(class_code = "635-41", sfaa_fidelity_loss_cost = .7, company_loss_cost = 1)
    exposure = Exposure.objects.get(pk = 134)
    agreementtype = AgreementType.objects.create(name = "Employee Dishonesty", mod_factor = 1)
    insuringagreement = InsuringAgreement.objects.create(insurance_limit = 1000000, deductible = 10000, agreement_type = agreementtype)
    accountinfo.save()
    riskdata.save()
    classcode.save()
    agreementtype.save()
    insuringagreement.save()
    cls.quote = Quote()
    cls.quote.underwriter = "JonnyTest"
    cls.quote.account_info = accountinfo
    cls.quote.risk_data = riskdata
    cls.quote.class_code = classcode
    cls.quote.save()
    cls.quote.insuring_agreements.add(insuringagreement)
    
  def test_calcPremium(cls):
    quote = cls.quote
    print models.Exposure.calc_exposure_units(quote.risk_data.employee_count, 10000000)
      