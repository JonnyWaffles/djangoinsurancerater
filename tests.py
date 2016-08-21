from djangoinsurancerater.models import * 
from django.test import TestCase
from datetime import date
import os, sys, csv
# Create your tests here.

class QuoterTestCase(TestCase):
  #fixtures = ["exposureRow134.json"]
  
  def setUp(cls):
    with open(os.path.join(sys.path[0], 'djangoinsurancerater/ExposureCSV.csv')) as f:
      reader = csv.reader(f)
      for row in reader:
        _, created = Exposure.objects.get_or_create(
        number_employees = row[1],
        insurance_limit = row[2],
        exposure_points = row[3],
        )
        
    accountinfo = AccountInfo.objects.create(name = "TestQuote", date = date(2016, 7, 18))
    riskdata = RiskData.objects.create(employee_count = 5, rateable_count = 5, locations = 1)
    classcode = ClassCode.objects.create(class_code = "635-41", sfaa_fidelity_loss_cost = decimal.Decimal(0.7), company_loss_cost = decimal.Decimal(1.0))
    agreementtype = AgreementType.objects.create(name = "Employee Dishonesty", mod_factor = 1.0)
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
    testagreement = quote.insuring_agreements.get(agreement_type__name="Employee Dishonesty")
    print testagreement.calc_agreement_premium(quote)
      