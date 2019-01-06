from django import template
from portal.models import *
import calendar
register = template.Library()

@register.simple_tag
def get_something(employee, date):
    try:
        atem = employee.attendance_set.get(Date=date).Value.Short_Name
    except:
        atem = '-'
    return atem

@register.simple_tag
def get_total_days(employee, month):
    months_list_numbers = ['...', 'January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December']
    my_month = int(months_list_numbers.index(month.split('-')[0]))
    my_year = int(month.split('-')[1])

    full_days = employee.attendance_set.filter(Value__Fixed_Name='Full_Day', Date__My_Date__month=my_month, Date__My_Date__year=my_year).count()
    half_days = employee.attendance_set.filter(Value__Fixed_Name__contains='Half_Day', Date__My_Date__month=my_month, Date__My_Date__year=my_year).count()/2
    worked_days = full_days+half_days
    return worked_days



@register.filter
def month_name(value):
    return calendar.month(value)