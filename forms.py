from django import forms
from djangoinsurancerater.models import AccountInfo, RiskData, InsuringAgreement, ClassCode

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
    fields = ['agreement_type', 'insurance_limit', 'deductible' ]

class ClassCodeSelectForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super(ClassCodeSelectForm, self).__init__(*args, **kwargs)
    if hasattr(self, 'instance'):
      self.fields['class_code'].widget.instance = self.instance
  
  class Meta:
    model = ClassCode
    fields = ['class_code']
        
    
  
  
