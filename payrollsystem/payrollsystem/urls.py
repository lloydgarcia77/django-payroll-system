"""payrollsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from payrollsystemapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.PayrollSystemIndexPage.as_view(), name="index"),

    path('payroll_system/login/', views.payroll_system_user_login, name="user_login"),
    path('payroll_system/logout/', auth_views.LogoutView.as_view(), name="logout"),

    path('payroll_system/registration/employee/', views.employee_registration_form, name="register_employee_page"),
    path('payroll_system/registration/employee/success', views.EmployeeRegistrationFormSuccess.as_view(), name="register_employee_page_success"),

    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('Payroll/manager/employees/', views.PayrollEmployeesPage.as_view(), name='employees_index_page'),
    path('Payroll/employees/sort_employees/', views.employee_sort_records, name='sort_faculty'),
    path('Payroll/employees/record_limit_employees/', views.employee_record_limiter, name="record_limit_faculty"),
    path('Payroll/employees/search_employees/', views.employee_search_filter, name="search_faculty"),
    path('Payroll/employees/paging_employees/', views.employee_paging, name="paging_faculty"),
    path('Payroll/employees/update_employees/<int:id>/', views.update_employee_form, name="update_employee"),
    path('Payroll/employees/delete_employees/<int:id>/', views.delete_employee_form, name="delete_employee"),
    path('Payroll/employees/create_payroll_bill/<int:id>/', views.create_employee_bill, name="create_payroll_bill"),
    path('Payroll/employees/payroll_employee_history/<int:id>/', views.employee_history_table, name="employee_payroll_history"),
    path('Payroll/employees/payroll_employee_history/payroll_detail/<int:pk>/<int:id>/', views.employee_history_table_detail, name="employee_payroll_detail"),

    path('Payroll/client_employee/index_page/', views.ClientEmployeeIndexPage.as_view(), name="client_index_page"),
    path('Payroll/client_employee/payroll_page/', views.ClientEmployeesPayrollPage.as_view(), name="client_employee_payroll_page"),
    path('Payroll/client_employee/payroll_page/detail/<int:id>/', views.client_employee_payroll_detail, name="client_employee_payroll_page_detail"),



]
