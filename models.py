from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from localflavor.us.models import USStateField
import decimal
import scipy.interpolate


# Create your models here.

class AccountInfo(models.Model):
  name = models.CharField(max_length=30)
  date = models.DateField(auto_now=True)
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

@python_2_unicode_compatible  
class ClassCode(models.Model):
  class_code = models.CharField(max_length=7, primary_key=True)
  sfaa_fidelity_loss_cost = models.DecimalField(max_digits=3, decimal_places=2)
  company_loss_cost = models.DecimalField(max_digits=3, decimal_places=2)
  def __str__(self):
    return self.class_code
  
@python_2_unicode_compatible  # only if you need to support Python 2  
class AgreementType(models.Model):
  name = models.CharField(max_length=30)
  mod_factor = models.DecimalField(max_digits=5, decimal_places=2)
  
  def __str__(self):
    return self.name
  
class ExposureManager(models.Manager):
  @classmethod
  def calc_exposure_units(self, employees, limit):
    from django.core.exceptions import ObjectDoesNotExist
    #if employees at limit does not return a value from the database return interpolated value.
    try:
      exposure = Exposure.objects.get(number_employees=employees, insurance_limit=limit)
      return decimal.Decimal(exposure.exposure_points)
    except ObjectDoesNotExist:
      employee_count_record_set = Exposure.objects.filter(number_employees=employees)
      #find two records, one for the greatest limit in the queryset less than X and one for the smallest limit in the queryset greater than X
      lower_bound = employee_count_record_set.filter(insurance_limit__lt=limit).order_by('-insurance_limit').first()
      upper_bound = employee_count_record_set.filter(insurance_limit__gt=limit).order_by('insurance_limit').first() 
      limit_interp = scipy.interpolate.interp1d([lower_bound.insurance_limit, upper_bound.insurance_limit], [lower_bound.exposure_points, upper_bound.exposure_points])
      answer = limit_interp(limit)
      return decimal.Decimal(float(answer))
    
class Exposure(models.Model):
  number_employees = models.PositiveIntegerField()
  insurance_limit = models.PositiveIntegerField()
  exposure_points = models.DecimalField(max_digits=7, decimal_places=2)
  objects = ExposureManager()
  
  class Meta:
        unique_together = (('number_employees', 'insurance_limit'),)  

@python_2_unicode_compatible  # only if you need to support Python 2      
class InsuringAgreement(models.Model):
  insurance_limit = models.PositiveIntegerField()
  deductible = models.PositiveIntegerField()
  agreement_type = models.ForeignKey(AgreementType, on_delete=models.CASCADE)
  quote = models.ForeignKey('Quote', on_delete=models.CASCADE, related_name='agreements') #Agreements belong to quotes
  
  def __str__(self):
    return '%s %s %s' % (self.agreement_type.name, self.insurance_limit, self.deductible)
  
  def calc_agreement_premium(self, quote):
    #Removed debugging print statements. The exposure values need to be entered and saved as Decimals.
    deductible_exposure = Exposure.objects.calc_exposure_units(quote.risk_data.employee_count, self.deductible) * decimal.Decimal('.85')
    total_exposure = Exposure.objects.calc_exposure_units(quote.risk_data.employee_count, self.insurance_limit + self.deductible) - deductible_exposure
    insuring_agreement_premium = total_exposure * quote.class_code.sfaa_fidelity_loss_cost * quote.class_code.company_loss_cost * self.agreement_type.mod_factor
    return decimal.Decimal(insuring_agreement_premium)
    
    
#class Pricing(models.Model):
  #pass
  
class Quote(models.Model):
  underwriter = models.CharField(max_length=30)
  created_time = models.DateField(auto_now_add=True)
  account_info = models.ForeignKey(AccountInfo, on_delete=models.CASCADE)
  class_code = models.ForeignKey(ClassCode, on_delete=models.CASCADE)
  risk_data = models.ForeignKey(RiskData, on_delete=models.CASCADE)
  #insuring_agreements = models.ManyToManyField(InsuringAgreement) #Trying to decide between using a FK on InsuringAgreement or ManytoMany, going with FK
  #pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)