from django.contrib import admin
from djangoinsurancerater.models import AccountInfo

# Register your models here.
class AccountInfoAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'date', 'entity_type']
  list_display_links = ['id', 'name', 'date', 'entity_type']
  
admin.site.register(AccountInfo, AccountInfoAdmin)