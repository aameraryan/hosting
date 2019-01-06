from django.contrib import admin
from .models import *

admin.site.site_header = 'Fine-Leap Systems'
admin.site.site_title = 'Fine-Leap Systems'


class ValueModelAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Short_Name', 'Point', 'Fixed_Name']


admin.site.register(ValueModel, ValueModelAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['Name']
    list_display = ['Name', 'DOJ', 'Employee_ID', 'Leave_Balance', 'CF_LB']
    list_filter = ['Leave_Balance', 'CF_LB']

class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ['Date', 'User']
    list_display = ['Date', 'User', 'Value']
    list_filter = ['Date' , 'User', 'Value']
    # raw_id_fields = ['Date']


class DateAdmin(admin.ModelAdmin):
    search_fields = ['My_Date']
    list_display = ['My_Date', 'all_presence', 'get_attendances']


admin.site.register(Date, DateAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Month_Leaves)





# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ['Name', ]
#
#
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ['AtDate', ]
#
#
# class AtMonthAdmin(admin.ModelAdmin):
#     list_display = ['Name', ]
#
#
# admin.site.register(Employee, EmployeeAdmin)
# admin.site.register(Attendance, AttendanceAdmin)
# admin.site.register(AtMonth, AtMonthAdmin)
#
