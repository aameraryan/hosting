from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, logout_then_login

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_attendance/$', views.add_attendance, name='add_attendance'),
    url(r'^add_any_attendance/$', views.add_any_attendance, name='add_any_attendance'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    path('calendar/<month_id>/', views.month_calendar, name='month_calendar'),
    url(r'^emp_refresh/$', views.emp_refresh, name='emp_refresh'),
    url(r'^add_month_leaves/$', views.add_month_leaves, name="add_month_leaves"),
    url(r'^login/$', LoginView.as_view(template_name='portal/portal_login.html'), name='login'),
    url(r'^employees', views.employees, name='employees'),
    url(r'^employee_months/(?P<employee_id>[0-9]+)/$', views.employee_months, name='employee_months'),
    path('employee_month_calendar/<month_id>/<employee_id>/', views.employee_month_calendar, name='employee_month_calendar'),
    url(r'^employee_details/(?P<employee_id>[0-9]+)/$', views.employee_details, name='employee_details'),
    url(r'^logout/$', logout_then_login, name='logout'),
]