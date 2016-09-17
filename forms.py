from django import forms
from djangoinsurancerater.models import AccountInfo, RiskData, InsuringAgreement, ClassCode, Quote

class AccountInfoForm(forms.ModelForm):
  class Meta:
    model = AccountInfo
    exclude = ['title']
    
class RiskDataForm(forms.ModelForm):
  class Meta:
    model = RiskData
    fields = '__all__'

class InsuringAgreementForm(forms.ModelForm):
  class Meta:
    model = InsuringAgreement
    fields = [ 'agreement_type', 'insurance_limit', 'deductible'] 
    localized_fields = ['insurance_limit', 'deductible'] 
    widgets = {'agreement_type': forms.HiddenInput(),}

class ClassCodeSelectForm(forms.ModelForm):
  class_code = forms.CharField(max_length=100)
  
  class Meta:
    model = ClassCode
    fields = ['class_code']

        
    
  
  
