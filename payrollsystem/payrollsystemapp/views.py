from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404
from django.db.models import Q, F, Sum, Value
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from payrollsystemapp.models import ProfileInfo, CompanyInfo, PersonalBenefits, EmployeePayroll
from payrollsystemapp.forms import EmployeeUserRegistration, EmployeeProfileRegistrationForm, CompanyRegistrationForm, PersonalBenefitsRegistrationForm, EmployeePayrollForm


class PayrollSystemIndexPage(LoginRequiredMixin, TemplateView):
    template_name = 'payroll_system_index_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PayrollSystemIndexPage, self).get_context_data(*args, **kwargs)
        try:
            user = User.objects.all().filter(Q(username=self.request.user) & Q(is_superuser=True))
            username = User.objects.all().get(Q(username=self.request.user) & Q(is_superuser=True))

            if not user:
                raise Http404()
        except User.DoesNotExist:
            raise Http404()

        context.update({
            'user': user,
            'username': username,
        })

        return context

def payroll_system_user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active and user.is_staff and user.is_superuser:
                request.session.set_expiry(300)
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            elif user.is_active and user.is_staff:
                request.session.set_expiry(300)
                login(request, user)
                return HttpResponseRedirect(reverse("client_index_page"))
            else:
                messages.warning(request, "Account Not Active")
        else:
            messages.error(request, "Invalid Account")

    return render(request, "registration/login.html")

def employee_registration_form(request):
    template_name = "registration/employee_registration_form.html"

    if request.method == "POST":
        emp_user_reg_form = EmployeeUserRegistration(data=request.POST)
        emp_prof_reg_form = EmployeeProfileRegistrationForm(data=request.POST)
        emp_comp_reg_form = CompanyRegistrationForm(data=request.POST)
        emp_pers_bene_reg_form = PersonalBenefitsRegistrationForm(data=request.POST)

        if emp_user_reg_form.is_valid() and emp_prof_reg_form.is_valid() and emp_comp_reg_form.is_valid() and emp_pers_bene_reg_form.is_valid():

            userForm = emp_user_reg_form.save(commit=False)
            userForm.is_active = False
            userForm.is_staff = False
            userForm.is_superuser = False
            userForm.save()

            profileForm = emp_prof_reg_form.save(commit=False)
            profileForm.user = userForm
            profileForm.save()

            companyForm = emp_comp_reg_form.save(commit=False)
            companyForm.comp_profile = profileForm
            companyForm.save()

            benefitsForm = emp_pers_bene_reg_form.save(commit=False)
            benefitsForm.pers_profile = profileForm
            benefitsForm.save()

            return HttpResponseRedirect(reverse("register_employee_page_success"))

        else:
            messages.error(request, 'Form Error!')

    else:
        emp_user_reg_form = EmployeeUserRegistration()
        emp_prof_reg_form = EmployeeProfileRegistrationForm()
        emp_comp_reg_form = CompanyRegistrationForm()
        emp_pers_bene_reg_form = PersonalBenefitsRegistrationForm()
    context = {
        "emp_user_reg_form": emp_user_reg_form,
        "emp_prof_reg_form": emp_prof_reg_form,
        "emp_comp_reg_form": emp_comp_reg_form,
        "emp_pers_bene_reg_form": emp_pers_bene_reg_form,
    }
    return render(request, template_name, context)

class EmployeeRegistrationFormSuccess(TemplateView):
    template_name = "registration/employee_registration_form_success.html"

class PayrollEmployeesPage(LoginRequiredMixin, TemplateView):
    template_name = "employees/employees_index_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PayrollEmployeesPage, self).get_context_data(*args, **kwargs)
        try:
            user = User.objects.all().filter(Q(username=self.request.user) & Q(is_superuser=True))
            username = User.objects.all().get(Q(username=self.request.user) & Q(is_superuser=True))
            if not user:
                raise Http404()
        except User.DoesNotExist:
            raise Http404()

        for key, value in self.request.session.items():
            print('{} -> {}'.format(key, value))

        if 'current_page' in self.request.session:
            del self.request.session['current_page']
            print('current_page => DELETED!')
        else:
            print('current_page is not existing yet!')

        if 'search_text' in self.request.session:
            del self.request.session['search_text']
            print('searched_text => DELETED!')
        else:
            print('searched_text is not existing yet')

        if 'sortBy' in self.request.session:
            del self.request.session['sortBy']
            print('sortBy => DELETED!')
        else:
            print('sortBy is not existing yet')

        if 'column' in self.request.session:
            del self.request.session['column']
            print('column => DELETED')
        else:
            print('column is not existing yet')

        if 'limit' in self.request.session:
            del self.request.session['limit']
            print('limit => DELETED')
        else:
            print('limit is not existing yet')

        query = ProfileInfo.objects.all().order_by('-id')
        count = query.count()
        query = employee_page_pagination(query, 10, 1)


        columns = []

        # for field in SubjectInfo._meta.get_fields()[1:]: # [exclude:include]skip first item for it's using foreign key
        for field in ProfileInfo._meta.get_fields()[3:]:
            col = field.get_attname_column()[1]
            columns.append(col.replace("_", " "))

        columns.remove("user id")
        columns.remove("suffix")
        columns.remove("dob")
        columns.remove("age")
        columns.remove("date added")

        context.update({
            "user": user,
            "query": query,
            "count": count,
            'columns': columns,
            'username': username,
        })

        return context

def employee_database_query(searched_text, sortBy, column):
    if sortBy is None or column is None:
        sortable = '-id'
    else:
        if sortBy.lower() == 'Ascending'.lower():
            sortable = column.lower()
        elif sortBy.lower() == 'Descending'.lower():
            sortable = '-' + column.lower()

    if searched_text:
        query = ProfileInfo.objects.filter(
            Q(first_name__icontains=searched_text) |
            Q(middle_name__icontains=searched_text) |
            Q(last_name__icontains=searched_text) |
            Q(gender__icontains=searched_text) |
            Q(address__icontains=searched_text) |
            Q(mobile_no__icontains=searched_text)
        ).distinct().order_by(sortable)
    else:
        query = ProfileInfo.objects.all().order_by(sortable)

    return query

def employee_page_pagination(query, limit, current_page=1):
    if current_page is None:
        current_page = 1

    paginator = Paginator(query, limit)

    try:
        new_query = paginator.page(current_page)
    except PageNotAnInteger:
        print('Error: ', PageNotAnInteger)
        new_query = paginator.page(1)
    except EmptyPage:
        print('Error: ', EmptyPage)
        new_query = paginator.page(paginator.num_pages)

    return new_query


def employee_filtered_query(request):
    searched_text = request.session.get('search_text') if request.session.get('search_text') is not None else False
    sortBy = request.session.get('sortBy') if request.session.get('sortBy') is not None else 'Descending'
    column = request.session.get('column') if request.session.get('column') is not None else 'id'
    limit = request.session.get('limit') if request.session.get('limit') is not None else 10
    current_page = request.session.get('current_page') if request.session.get('current_page') is not None else 1

    print('SEARCHED: ', searched_text)
    print('SORT BY: ', sortBy)
    print('COLUMN: ', column.lower().replace(" ", "_"))
    print('LIMIT: ', limit)
    print('CURRENT PAGE: ', current_page)

    query = employee_database_query(searched_text, sortBy, column.lower().replace(" ", "_"))
    count = query.count()

    new_query = employee_page_pagination(query, limit, current_page)

    return new_query, count

def employee_search_filter(request):
    if request.method == 'GET' and request.is_ajax():
        data = dict()

        request.session['search_text'] = request.GET.get('search_text')

        new_query, count = employee_filtered_query(request)

        context = {
            'query': new_query,
            'count': count,
        }

        data['employee_table_records'] = render_to_string('employees/employee_table.html', context)
        data['employee_pagination'] = render_to_string('employees/employee_pagination.html', context)

        return JsonResponse(data)
    else:
        # value error when directly to url not ajax request
        raise Http404()

def employee_record_limiter(request):
    if request.method == 'GET' and request.is_ajax():

        data = dict()

        request.session['limit'] = request.GET.get('limit')

        new_query, count = employee_filtered_query(request)

        context = {
            'query': new_query,
            'count': count,
        }

        data['employee_table_records'] = render_to_string('employees/employee_table.html', context)
        data['employee_pagination'] = render_to_string('employees/employee_pagination.html', context)

        return JsonResponse(data)
    else:
        # value error when directly to url not ajax request
        raise Http404()

def employee_sort_records(request):
    if request.method == 'GET' and request.is_ajax():
        data = dict()

        request.session['sortBy'] = request.GET.get('sortBy')
        request.session['column'] = request.GET.get('column')

        new_query, count = employee_filtered_query(request)

        context = {
            'query': new_query,
            'count': count,
        }

        data['employee_table_records'] = render_to_string('employees/employee_table.html', context)
        data['employee_pagination'] = render_to_string('employees/employee_pagination.html', context)

        return JsonResponse(data)
    else:
        # value error when directly to url not ajax request
        raise Http404()

def employee_paging(request):
    if request.method == 'GET' and request.is_ajax():

        data = dict()

        request.session['current_page'] = request.GET.get('page')

        new_query, count = employee_filtered_query(request)

        context = {
            'query': new_query,
            'count': count,
        }

        data['employee_table_records'] = render_to_string('employees/employee_table.html', context)
        data['employee_pagination'] = render_to_string('employees/employee_pagination.html', context)

        return JsonResponse(data)
    else:
        # value error when directly to url not ajax request
        raise Http404()

def update_employee_form(request, id):
    data = dict()
    template_name = "employees/employees_update_form.html"
    profile = get_object_or_404(ProfileInfo, id=id)
    company = get_object_or_404(CompanyInfo, comp_profile=profile)
    benefits = get_object_or_404(PersonalBenefits, pers_profile=profile)

    if request.is_ajax():
        if request.method == "POST":
            emp_prof_reg_form = EmployeeProfileRegistrationForm(request.POST, instance=profile)
            emp_comp_reg_form = CompanyRegistrationForm(request.POST, instance=company)
            emp_pers_bene_reg_form = PersonalBenefitsRegistrationForm(request.POST, instance=benefits)
            if emp_prof_reg_form.is_valid() and  emp_comp_reg_form.is_valid() and emp_pers_bene_reg_form.is_valid():

                emp_prof_reg_form.save()
                emp_comp_reg_form.save()
                emp_pers_bene_reg_form.save()

                new_query, count = employee_filtered_query(request)

                context = {
                    'query': new_query,
                    'count': count,
                }

                data['employee_table_records'] = render_to_string('employees/employee_table.html', context)
                data['employee_pagination'] = render_to_string('employees/employee_pagination.html', context)

                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
        elif request.method == "GET":
            emp_prof_reg_form = EmployeeProfileRegistrationForm(instance=profile)
            emp_comp_reg_form = CompanyRegistrationForm(instance=company)
            emp_pers_bene_reg_form = PersonalBenefitsRegistrationForm(instance=benefits)

        context = {
            'profile': profile,
            'emp_prof_reg_form': emp_prof_reg_form,
            'emp_comp_reg_form': emp_comp_reg_form,
            'emp_pers_bene_reg_form': emp_pers_bene_reg_form,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()

def delete_employee_form(request, id):
    data = dict()
    template_name = "employees/employees_delete_form.html"
    record = get_object_or_404(ProfileInfo, id=id)

    if request.is_ajax():
        if request.method == "POST":
            user = User.objects.all().get(profile_to_user_fk=record)
            user.delete()

            new_query, count = employee_filtered_query(request)

            context = {
                'query': new_query,
                'count': count,
            }

            data['employee_table_records'] = render_to_string('employees/employee_table.html', context)
            data['employee_pagination'] = render_to_string('employees/employee_pagination.html', context)

            data['form_is_valid'] = True

        elif request.method == "GET":
            context = {
                'record': record,
            }
            data['html_form'] = render_to_string(template_name, context, request)
        return JsonResponse(data)

    else:
        raise Http404()



def create_employee_bill(request, id):
    data = dict()
    template_name = "employees/employee_payroll_page.html"
    employee = get_object_or_404(ProfileInfo, id=id)

    if request.is_ajax():
        if request.method == "POST":
             form = EmployeePayrollForm(request.POST)
             if form.is_valid():
                 instance = form.save(commit=False)
                 instance.employee = employee
                 instance.save()

                 data['form_is_valid'] = True
             else:
                 data['form_is_valid'] = False
        elif request.method == "GET":
            form = EmployeePayrollForm()

        context = {
            "employee": employee,
            "form": form,
        }

        data['html_form'] = render_to_string(template_name, context, request)

        return JsonResponse(data)
    else:
        raise Http404()

def employee_history_table(request, id):
    data = dict()
    template_name = "employees/employee_payroll_history.html"
    employee = get_object_or_404(ProfileInfo, id=id)
    query = EmployeePayroll.objects.all().filter(employee=id).order_by('-id')

    if request.is_ajax():
        if request.method == "GET":
            context = {
                "query": query,
                "records": employee,
            }
            data['html_form'] = render_to_string(template_name, context, request)

            return JsonResponse(data)
    else:
        raise Http404()

def employee_history_table_detail(request, pk, id):
    data = dict()
    template_name = "employees/employee_payroll_history_table_detail.html"
    employee_profile = get_object_or_404(ProfileInfo, id=pk)
    employee_detail = get_object_or_404(EmployeePayroll, employee=employee_profile, id=id)

    if request.is_ajax():
        if request.method == "GET":
            context = {
                "employee_profile": employee_profile,
                "employee_detail": employee_detail,
            }
            data['html_form'] = render_to_string(template_name, context, request)

            return JsonResponse(data)
    else:
        Http404()
# ==========================================================


class ClientEmployeeIndexPage(LoginRequiredMixin, TemplateView):
    template_name = "client-employees/client_employee_index_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ClientEmployeeIndexPage, self).get_context_data(*args, **kwargs)
        try:
            user = User.objects.all().filter(username=self.request.user)
            profile = ProfileInfo.objects.all().get(user__in=user)
        except User.DoesNotExists:
            raise Http404()

        context.update({
            'user': user,
            'profile': profile,
        })

        return context


class ClientEmployeesPayrollPage(LoginRequiredMixin, TemplateView):
    template_name = "client-employees/client_employee_payroll_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ClientEmployeesPayrollPage, self).get_context_data(*args, **kwargs)
        try:
            user = User.objects.all().filter(username=self.request.user)
            username = User.objects.all().get(username=self.request.user)
            profile = ProfileInfo.objects.all().get(user__in=user)
            query = EmployeePayroll.objects.all().filter(employee=profile).order_by('-id')
            if not user:
                raise Http404()
        except User.DoesNotExist:
            raise Http404()

        context.update({
            "user": user,
            "username": username,
            "profile": profile,
            "query": query,
        })

        return context


def client_employee_payroll_detail(request, id):
    data = dict()
    template_name = "client-employees/client_employeee_payroll_detail.html"
    employee_detail = get_object_or_404(EmployeePayroll, id=id)

    if request.is_ajax():
        if request.method == "GET":
            context = {
                "employee_detail": employee_detail,
            }
            data['html_form'] = render_to_string(template_name, context, request)

            return JsonResponse(data)
    else:
        Http404()