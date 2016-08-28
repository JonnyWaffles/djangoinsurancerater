from django.forms import ModelForm
from djangoinsurancerater.models import AccountInfo

class AccountInfoForm(ModelForm):
  class Meta:
    model = AccountInfo
    fields = ['name', 'rating_state', 'entity_type']