from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Quote(models.Model):
  underwriter = models.CharField(max_length=30)
  createdTime = models.DateField(auto_now_add=True)
  accountInfo = models.ForeignKey(AccountInfo, on_delete=models.CASCADE)
  classCode = models.ForeignKey(ClassCode, on_delete=models.CASCADE)
  riskData = models.ForeignKey(RiskData, on_delete=models.CASCADE)
  employeeDishonesty = models.ForeignKey(EmployeeDishonesty, on_delete=models.CASCADE)
  sfaaSubAgreements = models.ForeignKey(SFAAsubAgreements, on_delete=models.CASCADE)
  pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)
  
class AccountInfo(models.Model):
  name = models.CharField(max_length=30)
  date = models.DateField()
  ratingState = models#making state choice list
  ENTITY_TYPES = (
    ('M', 'Mercantile'),
    ('G', 'Governmental'),
  )
  entityType = models.CharField(max_length=1, choices=ENTITY_TYPES)
  
class ClassCode(models.Model):

class RiskData(models.Model):
  employeeCount = models.PositiveIntegerField()
  rateableCount = models.PositiveIntegerField()
  
class EmployeeDishonesty(InsuringAgreement):
  locations = models.PositiveIntegerField()
  
class Forgery(InsuringAgreement):
  
class Inside(InsuringAgreement):

class Outside(InsuringAgreement):

class ComputerFraud(InsuringAgreement):

class Counterfeit(InsuringAgreement):
  
class ClientsProperty(InsuringAgreement):

class FundsTransfer(InsuringAgreement):
  
class FraudulentlyInducedTransfer(InsuringAgreement):

class InsuringAgreement(models.Model):
  limit = models.PositiveIntegerField()
  deductible = models.PositiveIntegerField()
  def __str__(self):
    return '%S %S %S' (self.__class__.__name__, self.limit, self.deductible) 
  
  class Meta:
    abstract = True
    