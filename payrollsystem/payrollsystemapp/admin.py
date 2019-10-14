from django.contrib import admin
from payrollsystemapp.models import ProfileInfo, CompanyInfo, PersonalBenefits, EmployeePayroll
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.site_header = 'Payroll System Administrator'
admin.site.index_title = 'Payroll System Administrator Page'
admin.site.site_title = 'Payroll Administrator Panel'


class ProfileAdmin(ImportExportModelAdmin):
    list_display = ("user", "first_name", "middle_name", "last_name", "suffix", "dob", "mobile_no", "age", "gender", "address", "date_added")
    list_editable = ("first_name", "middle_name", "last_name", "suffix", "dob", "mobile_no", "age", "gender", "address")
    list_per_page = 10
    search_fields = ("first_name", "middle_name", "last_name", "suffix", "dob", "mobile_no")
    list_filter = ("first_name", "middle_name", "last_name", "suffix")


admin.site.register(ProfileInfo, ProfileAdmin)

class CompanyAdmin(ImportExportModelAdmin):
    list_display = ("comp_profile", "company_id", "company_tin", "designation", "department",)
    list_editable = ("company_id", "company_tin", "designation", "department",)
    list_per_page = 10
    search_fields = ("company_id", "company_tin", "designation", "department",)
    list_filter = ("company_id", "company_tin", "designation", "department",)

admin.site.register(CompanyInfo, CompanyAdmin)

class PersonalBenefitsAdmin(ImportExportModelAdmin):
    list_display = ("pers_profile", "tin", "sss", "pagibig", "philhealth",)
    list_editable = ("tin", "sss", "pagibig", "philhealth",)
    list_per_page = 10
    search_fields = ("tin", "sss", "pagibig", "philhealth",)
    list_filter = ("tin", "sss", "pagibig", "philhealth",)

admin.site.register(PersonalBenefits, PersonalBenefitsAdmin)

class EmployeePayrollAdmin(ImportExportModelAdmin):
    list_display = ("employee", "payroll_cut_off_period_from","payroll_cut_off_period_to","payroll_date","monthly_rate","monthly_allowance","basic_pay","allowance","overtime_pay","legal_holiday","special_holiday","late_or_absences","salary_or_cash_advance","gross_pay","sss_premiums","philhealth_contribution","pagibig_contribution","withholding_tax","pagibig_loan","total_deduction","net_pay", "date_added", )
    list_editable = ("payroll_cut_off_period_from","payroll_cut_off_period_to","payroll_date","monthly_rate","monthly_allowance","basic_pay","allowance","overtime_pay","legal_holiday","special_holiday","late_or_absences","salary_or_cash_advance","gross_pay","sss_premiums","philhealth_contribution","pagibig_contribution","withholding_tax","pagibig_loan","total_deduction","net_pay",)
    list_per_page = 10
    search_fields = ("payroll_cut_off_period_from","payroll_cut_off_period_to","payroll_date",)
    list_filter = ("payroll_cut_off_period_from","payroll_cut_off_period_to","payroll_date",)

admin.site.register(EmployeePayroll, EmployeePayrollAdmin)