from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
# Create your models here.


class ProfileInfo(models.Model):

    GENDER_LIST = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_to_user_fk", default="lloyd.garcia")

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField()
    mobile_no = models.CharField(max_length=20, unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=50, choices=GENDER_LIST, default='Male')
    address = models.CharField(max_length=250)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.last_name + " " + self.first_name + " " + self.middle_name)

class CompanyInfo(models.Model):

    comp_profile = models.OneToOneField(ProfileInfo, on_delete=models.CASCADE, related_name="company_to_profile_fk", null=True)
    company_id = models.CharField(max_length=50, unique=True)
    company_tin = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):
        return str(self.company_id)

class PersonalBenefits(models.Model):

    pers_profile = models.OneToOneField(ProfileInfo, on_delete=models.CASCADE, related_name="benefits_to_profile_fk", null=True)
    tin = models.CharField(max_length=50, unique=True)
    sss = models.CharField(max_length=50, unique=True)
    pagibig = models.CharField(max_length=50, unique=True)
    philhealth = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.pers_profile)

class EmployeePayroll(models.Model):
    employee = models.ForeignKey(ProfileInfo, on_delete=models.CASCADE, related_name="payroll_employee_fk", null=True)
    payroll_cut_off_period_from = models.DateField()
    payroll_cut_off_period_to = models.DateField()
    payroll_date = models.DateField()
    monthly_rate = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    monthly_allowance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    basic_pay = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    allowance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    overtime_pay = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    legal_holiday = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    special_holiday = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    late_or_absences = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    salary_or_cash_advance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    gross_pay = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    #deductions
    sss_premiums = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    philhealth_contribution = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    pagibig_contribution = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    withholding_tax = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    pagibig_loan = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    total_deduction = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    net_pay = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    date_added = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.employee)

    #add save that will get sum of multuple columns
    #Foo.objects.annotate(i_sum=F('i1') + F('i2')+ F('i3')).filter(i_sum=200)
    #https://docs.djangoproject.com/en/1.10/topics/db/queries/#using-f-expressions-in-filters
    #https://docs.djangoproject.com/en/1.10/topics/db/queries/#using-f-expressions-in-filters
    """
    from django.db.models import F

    Task.objects.aggregate(total=Sum(F('progress') * F('estimated_days')))['total']
    from django.db.models import Value

    Task.objects.aggregate(total=Sum('progress') / Value(10))['total']
    
    
                 total = EmployeePayroll.objects.aggregate(total=Sum(F('basic_pay') + F('allowance')))['total']
                 print("-----", total)
    
    """


