from django.shortcuts import render, get_list_or_404, reverse
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.contrib import messages


def home(request):
    if request.user.is_authenticated:
        if Month_Leaves.objects.count() != 0:
            try:
                last_added = Month_Leaves.objects.first().Last_Added.month
            except:
                last_added = 'not added yet'
            this_month = datetime.date.today().month
            if last_added != this_month:
                context = {'show_add_leave': 1}
            else:
                context = {'show_add_leave': 2}
        else:
            context = {'show_add_leave': 1}
        date_check = Date.objects.filter(My_Date=datetime.date.today()).count()
        if date_check > 0:
            make_add = False
        else:
            make_add = True
        context.update({'make_add': make_add})
        return render(request, 'portal/home.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def emp_refresh(request):
    for employee in Employee.objects.all():
        employee.save()
    messages.success(request, "Successfully Refreshed the protal on {0}".format(datetime.date.today()))
    return HttpResponseRedirect(reverse('home'))
    # return render(request, 'portal/home.html', {'messages':('Successfully Refreshed the protal on {0}'.format(datetime.date.today()),)})


@login_required
def add_attendance(request):
    if request.method=='POST':
        att_date = Date.objects.create(My_Date=datetime.date.today())
        for input_name in request.POST:
            if '--' in input_name:
                emp = Employee.objects.get(id=str(input_name.split('--')[-1]))
                # emp_value = float(request.POST[input_name])
                if request.POST[input_name] == '0.0':
                    if emp.Leave_Balance < 1:
                        emp_value = ValueModel.objects.get_or_create(Fixed_Name='Unpaid_Leave')[0]
                    else:
                        emp_value = ValueModel.objects.get_or_create(Fixed_Name='Paid_Leave')[0]
                elif request.POST[input_name] == '0.5':
                    if emp.Leave_Balance < 0.5:
                        emp_value = ValueModel.objects.get_or_create(Fixed_Name='Unpaid_Half_Day')[0]
                    else:
                        emp_value = ValueModel.objects.get_or_create(Fixed_Name='Paid_Half_Day')[0]
                else:
                    emp_value = ValueModel.objects.get_or_create(Point=float(request.POST[input_name]))[0]
                Attendance.objects.create(Date=att_date, User=emp, Value=emp_value)
        messages.success(request, 'Successfully added Attendance of {date}'.format(date=att_date.My_Date))
        return HttpResponseRedirect(reverse('home'))
        # return render(request, 'portal/home.html', {'messages': ('Successfully added Attendance of {date}'.format(date=att_date.My_Date),)})
    else:
        return render(request, 'portal/add_attendance.html', {'employees': Employee.objects.all()})



@login_required
def add_any_attendance(request):
    if request.method=='POST':
        att_date = Date.objects.create(My_Date=request.POST['date'])
        for input_name in request.POST:
            if '--' in input_name:
                emp = Employee.objects.get(id=str(input_name.split('--')[-1]))
                # emp_value = float(request.POST[input_name])
                if request.POST[input_name] == '0.0':
                    if emp.Leave_Balance < 1:
                        emp_value = ValueModel.objects.get_or_create(Fixed_Name='Unpaid_Leave')[0]
                    else:
                        emp_value = ValueModel.objects.get_or_create(Fixed_Name='Paid_Leave')[0]
                elif request.POST[input_name] == '0.5':
                    if emp.Leave_Balance < 0.5:
                        emp_value = ValueModel.objects.get_or_create(Fixed_Name='Unpaid_Half_Day')[0]
                    else:
                        emp_value = ValueModel.objects.get_or_create(Fixed_Name='Paid_Half_Day')[0]
                else:
                    emp_value = ValueModel.objects.get_or_create(Point=float(request.POST[input_name]))[0]
                Attendance.objects.create(Date=att_date, User=emp, Value=emp_value)
        messages.success(request, 'Successfully added Attendance of {date}'.format(date=att_date.My_Date))
        return HttpResponseRedirect(reverse('home'))
        # return render(request, 'portal/home.html', {'messages': ('Successfully added Attendance of {date}'.format(date=att_date.My_Date),)})
    else:
        json_dates = json.dumps([str(date.My_Date) for date in Date.objects.all()])
        return render(request, 'portal/add_any_attendance.html', {'employees': Employee.objects.all(), 'json_dates': json_dates})





@login_required
def calendar(request):
    all_months = {date.My_Date.strftime("%B-%Y") for date in Date.objects.all().distinct()}
    return render(request, 'portal/calendar.html', {'all_months': all_months})

@login_required
def month_calendar(request, month_id):
    months_list_numbers = ['...', 'January', 'February', 'March', 'April', 'May','June',
                           'July', 'August', 'September', 'October', 'November', 'December']
    my_month = int(months_list_numbers.index(month_id.split('-')[0]))
    my_year = int(month_id.split('-')[1])
    dates = Date.objects.filter(My_Date__month=my_month, My_Date__year=my_year).order_by('My_Date')
    employees = Employee.objects.all()
    return render(request, 'portal/month_attendances.html', {'employees': employees,
                                                            'dates': dates, 'month': month_id})


@login_required
def add_month_leaves(request):
    try:
        last_added = Month_Leaves.objects.first().Last_Added.month
    except:
        Month_Leaves.objects.create()
        last_added = 'no month added'
    this_month = datetime.date.today().month
    if last_added != this_month:
        count = 0
        for employee in Employee.objects.all():
            if employee.DOJ < datetime.date.today()-datetime.timedelta(days=90):
                employee.CF_LB += 1.5
                employee.save()
                count += 1
        last_month_leave = Month_Leaves.objects.first()
        last_month_leave.Last_Added = datetime.date.today()
        last_month_leave.Added_Times += 1
        last_month_leave.save()
        messages.success(request, 'Successfully added month leaves to {0} employees.'.format(count))
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.success(request, 'Already added for this month')
        return HttpResponseRedirect(reverse('home'))

@login_required
def employees(request):
    return render(request, 'portal/employees.html', {'employees': Employee.objects.all()})

@login_required
def employee_months(request, employee_id):
    emp = Employee.objects.get(id=employee_id)
    employee_months = set()
    for att in emp.attendance_set.all():
        employee_months.add(att.Date.My_Date.strftime("%B-%Y"))
    # all_months = {date.My_Date.strftime("%B-%Y")  for date in Date.objects.all().distinct()}
    return render(request, 'portal/employee_months.html', {'employee_months': employee_months, 'employee': emp})


@login_required
def employee_month_calendar(request, month_id, employee_id):
    months_list_numbers = ['...', 'January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December']
    my_month = int(months_list_numbers.index(month_id.split('-')[0]))
    my_year = int(month_id.split('-')[1])
    dates = Date.objects.filter(My_Date__month=my_month, My_Date__year=my_year).order_by('My_Date')
    emp = Employee.objects.get(id=employee_id)
    attendances = Attendance.objects.filter(User=emp, Date__My_Date__month=my_month, Date__My_Date__year=my_year)
    working_days = dates.count()
    full_days = emp.attendance_set.filter(Date__My_Date__month=my_month, Date__My_Date__year=my_year, Value__Fixed_Name='Full_Day').count()
    paid_half_days = emp.attendance_set.filter(Date__My_Date__month=my_month, Date__My_Date__year=my_year, Value__Fixed_Name='Paid_Half_Day').count()
    unpaid_half_days = emp.attendance_set.filter(Date__My_Date__month=my_month, Date__My_Date__year=my_year, Value__Fixed_Name='Unpaid_Half_Day').count()
    paid_leaves = emp.attendance_set.filter(Date__My_Date__month=my_month, Date__My_Date__year=my_year, Value__Fixed_Name='Paid_Leave').count()
    unpaid_leaves = emp.attendance_set.filter(Date__My_Date__month=my_month, Date__My_Date__year=my_year, Value__Fixed_Name='Unpaid_Leave').count()
    work_days = full_days+(paid_half_days/2)+(unpaid_half_days/2)
    return render(request, 'portal/employee_month_calendar.html', {'employee': emp, 'attendances': attendances, 'dates':dates, 'month': month_id,
                                                                   'working_days': working_days, 'full_days': full_days, 'unpaid_half_days': unpaid_half_days,
                                                                   'paid_half_days': paid_half_days, 'paid_leaves': paid_leaves, 'unpaid_leaves': unpaid_leaves,
                                                                   'work_days': work_days,
                                                                   })


@login_required
def employee_details(request, employee_id):
    emp = Employee.objects.get(id=employee_id)
    return render(request, 'portal/employee_details.html', {'employee': emp})