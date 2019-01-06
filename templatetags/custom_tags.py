from django import template
from portal.models import *
import calendar
register = template.Library()

@register.simple_tag
def get_something(employee, date):
    try:
        atem = employee.attendance_set.get(Date=date).Value
    except:
        atem = '-'
    return atem

@register.filter
def month_name(value):
    return calendar.month(value)