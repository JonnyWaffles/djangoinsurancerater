from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from localflavor.us.models import USStateField
import scipy.interpolate


# Create your models here.

class AccountInfo(models.Model):
  name = models.CharField(max_length=30)
  date = models.DateField()
  rating_state = USStateField(null=True, blank=True)
  ENTITY_TYPES = (
    ('M', 'Mercantile'),
    ('G', 'Governmental'),
  )
  entity_type = models.CharField(max_length=1, choices=ENTITY_TYPES)
  
class RiskData(models.Model):
  employee_count = models.PositiveIntegerField()
  rateable_count = models.PositiveIntegerField()
  locations = models.PositiveIntegerField()
  
  
class AgreementType(models.Model):
  name = models.CharField(max_length=30)
  mod_factor = models.DecimalField(max_digits=5, decimal_places=2)

class InsuringAgreement(models.Model):
  insurance_limit = models.PositiveIntegerField()
  deductible = models.PositiveIntegerField()
  agreement_type = models.ForeignKey(AgreementType, on_delete=models.CASCADE)
  def __str__(self):
    return '%S %S %S' (self.agreementType, self.limit, self.deductible) 
  
class Exposure(models.Model):
  number_employees = models.PositiveIntegerField()
  insurance_limit = models.PositiveIntegerField()
  exposure_points = models.DecimalField(max_digits=7, decimal_places=2)
  
  class Meta:
        unique_together = (('number_employees', 'insurance_limit'),)
  
  def calc_exposure_units(self, employees, limit):
    from django.core.exceptions import ObjectDoesNotExist
    #if employees at limit does not return a value from the database return interpolated value. Exposure.objects.filter(insurance_limit=limit)...
    try:
      exposure = Exposure.objects.get(number_employees=employees, insurance_limit=limit)
      return exposure.exposure_points
    except ObjectDoesNotExist:
      employee_count_record_set = Exposure.objects.filter(number_employees=employees)
      #find two records, one for the greatest limit in the queryset less than X and one for the smallest limit in the queryset greater than X
      lower_bound = employee_count_record_set.filter(insurance_limit__lt=limit).order_by('-insurance_limit').first()
      upper_bound = employee_count_record_set.filter(insurance_limit__gt=limit).order_by('insurance_limit').first() 
      limit_interp = scipy.interpolate.interp1d([lower_bound.insurance_limit, upper_bound.insurance_limit], [lower_bound.exposure_points, upper_bound.exposure_points])
      return limit_interp(limit)

class ClassCode:
  class_code = models.CharField(max_length=7, primary_key=True)
  sfaa_fidelity_loss_cost = models.DecimalField("SFAA Fidelity and Forgery Loss Cost", max_digits=3, decimal_places=2)
  company_loss_cost = models.DecimalField("Loss Cost Multiplier", max_digits=3, decimal_places=2)
    
class Pricing(models.Model):
  pass                                               
  #deductible_exposure = Exposure.calc_exposure_units(InsuringAgreement.deductible) * .85
  #total_exposure = Exposure.calc_exposure_units(InsuringAgreement.insurance_limit+InsuringAgreement.deductible) - deductible_exposure
  #insuring_agreement_name_premium = total_exposure * ClassCode.sfaa_fidelity_loss_cost * ClassCode.company_loss_cost * agreementType.mod_factor
  
class Quote(models.Model):
  underwriter = models.CharField(max_length=30)
  created_time = models.DateField(auto_now_add=True)
  account_info = models.ForeignKey(AccountInfo, on_delete=models.CASCADE)
  class_code = models.ForeignKey(ClassCode, on_delete=models.CASCADE)
  risk_data = models.ForeignKey(RiskData, on_delete=models.CASCADE)
  insuring_agreements = models.ManyToManyField(InsuringAgreement)
  pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)