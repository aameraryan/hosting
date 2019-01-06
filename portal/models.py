import math
from django.db import models
from django.db.models.signals import post_save, pre_save, post_init
from django.utils import timezone
import datetime
from django.http import HttpResponse


class ValueModel(models.Model):
    Name = models.CharField(max_length=20)
    Short_Name = models.CharField(max_length=5)
    Point = models.FloatField(default=0.0)
    Fixed_Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Date(models.Model):
    My_Date = models.DateField(unique=True)

    @property
    def getting_day(self):
        return str(self.My_Date.day)+' / '+str(self.My_Date.month)

    def __str__(self):
        return str(self.My_Date)

    def get_attendances(self):
        all_atts = self.attendance_set.all().order_by('User_id')
        all_atts_string = ''
        for att in all_atts:
            all_atts_string += f'{att.User.Name}:{att.Value.Short_Name} | '
        return all_atts_string

    def all_presence(self):
        full_days = self.attendance_set.filter(Value__Fixed_Name='Full_Day').count()
        half_days = self.attendance_set.filter(Value__Fixed_Name='Half_Day').count()
        paid_leaves = self.attendance_set.filter(Value__Fixed_Name='Paid_Leave').count()
        unpaid_leaves = self.attendance_set.filter(Value__Fixed_Name='Unpaid_Leave').count()

        return f'Full Days : {full_days} | Half Days : {half_days} | Paid Leaves : {paid_leaves} | Unpaid Leaves : {unpaid_leaves}'


class Employee(models.Model):
    Name = models.CharField(max_length=200)
    DOJ = models.DateField(null=True, blank=True, verbose_name='Date Of Joining.')
    Employee_ID = models.CharField(max_length=20, blank=True, null=True)
    CF_LB = models.FloatField(verbose_name='Carry Forward Leave Balance', default=0)
    Leave_Balance = models.FloatField(default=0)

    def __str__(self):
        return self.Name

    def total_days(self):
        return self.attendance_set.count()

    def total_worked_days(self):
        return self.attendance_set.filter(Value__Fixed_Name='Full_Day').count()+(self.attendance_set.filter(Value__Fixed_Name__contains='Half_Day').count()/2)

    def employment_duration(self):
        total_days = (datetime.date.today()-self.DOJ).days
        # total_days_string = '{2} days || approx {0} months and {1} days'.format(total_days//30, total_days%30, round(total_days/30, 2))
        total_days_string = '{0} days || approx {1} months'.format(total_days, round(total_days/30, 2))

        return total_days_string

class Attendance(models.Model):
    Date = models.ForeignKey(Date, on_delete=models.CASCADE, null=True, blank=True)
    User = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Employee')
    Value = models.ForeignKey(ValueModel, on_delete=models.PROTECT, verbose_name='value')

    def __str__(self):
        return "{0} | {1} | {2}".format(self.Date.My_Date, self.User, self.Value.Point)


def unpaid_leave_save(sender, instance, *args, **kwargs):
    paid_leave_value = ValueModel.objects.get_or_create(Fixed_Name='Paid_Leave')[0]
    if instance.Value == paid_leave_value and instance.User.Leave_Balance < 1:
        instance.Value = ValueModel.objects.get_or_create(Name='Unpaid_Leave')[0]
        instance.save()
post_save.connect(unpaid_leave_save, sender=Attendance)
# post_init.connect(unpaid_leave_save, sender=Attendance)


def date_save(sender, instance, **kwargs):
    if not instance.Date:
        today_date = Date.objects.get_or_create(My_Date=datetime.date.today())[0]
        instance.Date = today_date
        instance.save()

post_save.connect(date_save, sender=Attendance)

def lb_auto_call(sender, instance, **kwargs):
    instance.User.save()
post_save.connect(lb_auto_call, sender=Attendance)
#
def lb_save(sender, instance, **kwargs):
    print('auto save')
    all_atts = instance.attendance_set.all().exclude(Value__Fixed_Name__in=('Unpaid_Leave', 'Unpaid_Half_Day'))
    # instance.nk()
    total_count = all_atts.count()
    atts_count = sum([i.Value.Point for i in all_atts])
    if instance.Leave_Balance != (instance.CF_LB + atts_count - total_count):
        instance.Leave_Balance = (instance.CF_LB + atts_count - total_count)
        instance.save()
pre_save.connect(lb_save, sender=Employee)


class Month_Leaves(models.Model):
    Last_Added = models.DateField(blank=True, null=True)
    Added_Times = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Last_Added)

