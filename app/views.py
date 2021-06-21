from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views import generic
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from app import serializers
from app.forms import CompanyForm, ProjectForm, EmployeeForm
from app.models import Company, Project, Employee
from app.permissions import IsEmployeeOrStaffOrReadOnly, IsEmployeeOrStaff


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('companies-list')
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


def companies_list(request):
    context = {'companies_set_id': 'all_companies'}
    return render(request, 'app/company_list.html', context)


def my_companies(request):
    context = {'companies_set_id': 'my_companies'}
    return render(request, 'app/company_list.html', context)


def projects_list(request):
    return render(request, 'app/project_list.html')


def company_employees(request, pk):
    company = Company.objects.get(id=pk)
    if company.employees.filter(role__in=('o', 'e')).filter(user__exact=request.user):
        context = {
            'company': company,
            'is_company_owner': bool(company.employees.filter(role__exact='o').filter(user__exact=request.user)),
        }
        return render(request, 'app/employee_list.html', context)
    else:
        return HttpResponseForbidden(
            b"You don't have permissions to view this company employees!\n<a href='/'>Back to site</a>")


class CompanyDetailView(generic.DetailView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)

        context['is_company_owner'] = bool(
            self.request.user.is_authenticated and
            self.get_object().employees.filter(role__exact='o').filter(user__exact=self.request.user)
        )
        context['is_employee'] = bool(
            self.request.user.is_authenticated and
            self.get_object().employees.filter(role__in=('o', 'e')).filter(user__exact=self.request.user)
        )
        return context


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['is_company_owner'] = bool(
            self.request.user.is_authenticated and
            self.get_object().company.employees.filter(role__exact='o').filter(user__exact=self.request.user)
        )
        context['is_company_employee'] = bool(
            self.request.user.is_authenticated and
            self.get_object().company.employees.filter(role__in=('o', 'e')).filter(user__exact=self.request.user)
        )
        return context


class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsEmployeeOrStaffOrReadOnly]


class CompanyView(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = serializers.CompanyProjectsSerializer
    permission_classes = [IsEmployeeOrStaffOrReadOnly]


class EmployeesView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = serializers.CompanyEmployeesSerializer
    permission_classes = [IsAdminUser]


class CompanyEmployees(RetrieveAPIView):
    serializer_class = serializers.CompanyEmployeesSerializer
    permission_classes = [IsEmployeeOrStaff]

    def get_queryset(self):
        return Company.objects.filter(id=self.kwargs['pk'])


class MyCompaniesView(ListAPIView):
    serializer_class = serializers.UserCompaniesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(employees__user__exact=self.request.user)


class CompanyCreateView(LoginRequiredMixin, generic.CreateView):
    model = Company
    form_class = CompanyForm
    login_url = '/auth/login/'


    def form_valid(self, form):
        company = form.save()
        owner = Employee(company=company, user=self.request.user, role='o')
        owner.save()
        return super(CompanyCreateView, self).form_valid(form)


class CompanyUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Company
    form_class = CompanyForm

    def has_permission(self):
        return bool(
            self.get_object().employees.filter(role__exact='o').filter(user__exact=self.request.user)
        )


class CompanyDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Company

    def has_permission(self):
        return bool(
            self.get_object().employees.filter(role__exact='o').filter(user__exact=self.request.user)
        )


class ProjectCreateView(generic.CreateView, LoginRequiredMixin):
    model = Project
    form_class = ProjectForm

    def get_form_class(self):
        form = super(ProjectCreateView, self).get_form_class()

        company = self.request.GET.get('company')
        if company is not None:
            form.base_fields['company'].initial = Company.objects.get(id=company)
        form.base_fields['company'].queryset = Company.objects.filter(employees__user__exact=self.request.user)
        return form


class ProjectUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm

    def get_form_class(self):
        form = super(ProjectUpdateView, self).get_form_class()
        form.base_fields['company'].queryset = Company.objects.filter(employees__user__exact=self.request.user)
        return form

    def has_permission(self):
        return bool(
            self.get_object().company.employees.filter(role__in=('o', 'e')).filter(user__exact=self.request.user)
        )


class ProjectDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Project

    def has_permission(self):
        return bool(
            self.get_object().company.employees.filter(role__exact='o').filter(user__exact=self.request.user)
        )


class EmployeeCreateView(PermissionRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeForm

    def get_form_class(self):
        form = super(EmployeeCreateView, self).get_form_class()
        form.base_fields['company'].queryset = Company.objects.filter(employees__user__exact=self.request.user)
        form.base_fields['company'].initial = Company.objects.get(id=self.kwargs['pk'])
        return form

    def form_valid(self, form):
        employee = form.save(commit=False)
        if employee.company.employees.filter(role__exact='o').filter(user=self.request.user):
            if not employee.company.employees.filter(user__exact=employee.user):
                employee.save()
            return redirect('company-employees', pk=self.kwargs['pk'])

        return HttpResponseForbidden(
            b"You don't have permissions to add employees to this company!\n<a href='/'>Back to site</a>")

    def has_permission(self):
        company = Company.objects.get(id=self.kwargs['pk'])

        return bool(company.employees.filter(role__exact='o').filter(user=self.request.user))


class EmployeeDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Employee

    def has_permission(self):
        employee = Employee.objects.get(id=self.kwargs['pk'])

        return bool(employee.company.employees.filter(role__exact='o').filter(user=self.request.user))

    def get_success_url(self):
        return reverse('company-employees', args=[str(self.get_object().company.id)])
