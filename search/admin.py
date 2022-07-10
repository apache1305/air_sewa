from django.contrib import admin
from .models import SearchConfig

# Register your models here.

class SearchConfigAdmin(admin.ModelAdmin):
    list_display = ('config_name', 'config_value',)
    search_fields = ('config_name',)

admin.site.register(SearchConfig, SearchConfigAdmin)
