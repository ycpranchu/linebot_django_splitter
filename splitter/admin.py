from django.contrib import admin

# Register your models here.
from splitter.models import *

class Main_Database_admin(admin.ModelAdmin):
    list_display = ('data_id', 'name_field', 'cost_field', 'time_field')

class Order_Data_admin(admin.ModelAdmin):
    list_display = ('order_id', 'Main_Database')

admin.site.register(Main_Database, Main_Database_admin)
admin.site.register(Order_Data, Order_Data_admin)