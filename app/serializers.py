from rest_framework import serializers

from app.models import Project, Company, Employee


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'logo_src', 'get_absolute_url']


class CompanyProjectsSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'city', 'description', 'logo_src', 'get_absolute_url', 'projects']


class EmployeeSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    # role = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['id', 'company', 'user', 'role_name']


class CompanyEmployeesSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['employees']


class UserCompaniesSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Company
        fields = ['name', 'city', 'logo_src', 'get_absolute_url']
