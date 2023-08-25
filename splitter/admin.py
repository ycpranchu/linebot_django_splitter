from django.contrib import admin

# Register your models here.
from splitter.models import *

class Main_Database_admin(admin.ModelAdmin):
    list_display = ('data_id', 'name_field', 'cost_field', 'time_field')

admin.site.register(Main_Database, Main_Database_admin)