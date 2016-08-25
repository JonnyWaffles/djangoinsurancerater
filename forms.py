from django.forms import ModelForm
from djangoinsurancerater import models

class AccountInfoForm(ModelForm):
  class Meta:
    model = AccountInfo
    fields = ['name', 'date', 'rating_state', 'entity_type']