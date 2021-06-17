from django.contrib import admin

# Register your models here.
from app.models import Country, City, Company, Employee, Project


class CityInline(admin.TabularInline):
    model = City
    extra = 0


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (CityInline,)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)


class ProjectsInline(admin.TabularInline):
    model = Project
    extra = 1


class EmployeesInline(admin.TabularInline):
    model = Employee
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')

    inlines = (ProjectsInline, EmployeesInline)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'company')
    list_filter = ('company',)
