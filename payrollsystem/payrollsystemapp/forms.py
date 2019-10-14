from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from decimal import Decimal
from payrollsystemapp.models import ProfileInfo, CompanyInfo, PersonalBenefits, EmployeePayroll

class EmployeeUserRegistration(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta():
        model = User
        fields = ("username", "email", "password1", "password2")


class EmployeeProfileRegistrationForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'width': "100%", 'cols': "80", 'rows': "5", }))

    dob = forms.DateField(
        widget=forms.DateInput(
            format='%b %d %Y',
            attrs={
                'id': 'dob',
            }
        ),
        input_formats=('%b %d %Y', )
    )

    class Meta():
        model = ProfileInfo
        exclude = ("user", "date_added")


class CompanyRegistrationForm(forms.ModelForm):

    class Meta():
        model = CompanyInfo
        exclude = ("comp_profile", )

class PersonalBenefitsRegistrationForm(forms.ModelForm):

    class Meta():
        model = PersonalBenefits
        exclude = ("pers_profile"),


class EmployeePayrollForm(forms.ModelForm):
    default_val = Decimal('0.00')
    monthly_rate = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    monthly_allowance = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    basic_pay = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    allowance = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    overtime_pay = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    legal_holiday = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    special_holiday = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    late_or_absences = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    salary_or_cash_advance = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)

    # deductions
    sss_premiums = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    philhealth_contribution = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    pagibig_contribution = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    withholding_tax = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)
    pagibig_loan = forms.DecimalField(max_digits=12, decimal_places=2, initial=default_val, required=True)

    payroll_cut_off_period_from = forms.DateField(
        widget=forms.DateInput(
            format='%b %d %Y',
            attrs={
                'id': 'payroll_cut_off_period_from',
            }
        ),
        input_formats=('%b %d %Y', )
    )

    payroll_cut_off_period_to = forms.DateField(
        widget=forms.DateInput(
            format='%b %d %Y',
            attrs={
                'id': 'payroll_cut_off_period_to',
            }
        ),
        input_formats=('%b %d %Y',)
    )

    payroll_date = forms.DateField(
        widget=forms.DateInput(
            format='%b %d %Y',
            attrs={
                'id': 'payroll_date',
            }
        ),
        input_formats=('%b %d %Y',)
    )

    class Meta():
        model = EmployeePayroll
        exclude = ("employee", "date_added",)
        #"gross_pay", "total_deduction", "net_pay",

    def __init__(self, *args, **kwargs):
        super(EmployeePayrollForm, self).__init__(*args, **kwargs)

        self.fields['gross_pay'].widget.attrs = {
            'readonly': 'readonly',
        }
        self.fields['total_deduction'].widget.attrs = {
            'readonly': 'readonly',
        }
        self.fields['net_pay'].widget.attrs = {
            'readonly': 'readonly',
        }


