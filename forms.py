from django.forms import ModelForm
from djangoinsurancerater.models import AccountInfo, RiskData, InsuringAgreement

class AccountInfoForm(ModelForm):
  class Meta:
    model = AccountInfo
    exclude = ['title']
    
class RiskDataForm(ModelForm):
  class Meta:
    model = RiskData
    fields = '__all__'

class InsuringAgreementForm(ModelForm):
  class Meta:
    model = InsuringAgreement
    fields = ['agreement_type', 'insurance_limit', 'deductible' ]
