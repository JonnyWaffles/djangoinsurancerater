from django.contrib import admin
from djangoinsurancerater.models import AccountInfo, RiskData, ClassCode, Quote

# Register your models here.
class AccountInfoAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'date', 'entity_type']
  list_display_links = ['id', 'name', 'date', 'entity_type']

class QuoteAdmin(admin.ModelAdmin):
  list_display = ['id', 'created_time', 'account_info', 'class_code']
  list_display_links = ['id', 'created_time', 'account_info', 'class_code']
  
admin.site.register(AccountInfo, AccountInfoAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(RiskData)
admin.site.register(ClassCode)