from django.contrib import admin
from.models import Hotel
# Register your models here.


class HostelAdmin(admin.ModelAdmin):
    
    list_display = ['hostel_name','location','price', 'stock','created_date','modified_date','is_available']
    
    prepopulated_fields = {'slug' : ('hostel_name',)}
    
admin.site.register(Hotel,HostelAdmin)