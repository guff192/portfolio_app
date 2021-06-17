from django.urls import path
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter

from app import views

router = SimpleRouter()
router.register('api/project', views.ProjectView, basename='project-api')
router.register('api/company', views.CompanyView, basename='company-api')
# router.register('api/employees/company', views.EmployeesView, basename='employee-api')


urlpatterns = [path('', RedirectView.as_view(url='companies/', permanent=True)),
    path('companies/', views.companies_list, name='companies-list'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('companies/<int:pk>/employees/', views.company_employees, name='company-employees'),
    path('companies/<int:pk>/add_employee/', views.EmployeeCreateView.as_view(), name='add-employee'),
    path('delete_employee/<int:pk>/', views.EmployeeDeleteView.as_view(), name='delete-employee'),
    path('my_companies/', views.my_companies, name='my-companies'),
    path('create_company/', views.CompanyCreateView.as_view(), name='create-company'),
    path('edit_company/<int:pk>/', views.CompanyUpdateView.as_view(), name='edit-company'),
    path('delete_company/<int:pk>/', views.CompanyDeleteView.as_view(), name='delete-company'),
    path('projects/', views.projects_list, name='projects-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('create_project/', views.ProjectCreateView.as_view(), name='create-project'),
    path('edit_project/<int:pk>', views.ProjectUpdateView.as_view(), name='edit-project'),
    path('delete_project/<int:pk>', views.ProjectDeleteView.as_view(), name='delete-project'),
    path('api/my_companies/', views.MyCompaniesView.as_view(), name='my-companies-api'),
    path('api/employees/', views.EmployeesView.as_view(), name='employee-api'),
    path('api/companies/<int:pk>/employees/', views.CompanyEmployees.as_view(), name='company-employees-api'), ]

urlpatterns += router.urls
