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
  #agreement_type = forms.ChoiceField(widget=forms.Select(attrs={'readonly'}))
  class Meta:
    model = InsuringAgreement
    fields = ['insurance_limit', 'deductible', 'premium'] 

class ClassCodeSelectForm(forms.ModelForm):
  class Meta:
    model = ClassCode
    fields = ['class_code']
        
    
  
  
