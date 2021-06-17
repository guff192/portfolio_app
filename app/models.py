from PIL import Image
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    name = models.CharField(max_length=128, help_text='Country', unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=128, help_text='City')
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.name}, {self.country}'


class Company(models.Model):
    name = models.CharField(max_length=128, help_text='Name of the company')
    description = models.TextField(max_length=5000, blank=True, help_text='Brief description of the company')
    city = models.ForeignKey(City, on_delete=models.RESTRICT, blank=True)

    employee = models.ManyToManyField(User, through='Employee')

    site = models.URLField(blank=True, help_text='Site of the company')
    phone = PhoneNumberField(blank=True, help_text='Company phone number')
    email = models.EmailField(blank=True, help_text='Company email')
    telegram = models.CharField(max_length=30, blank=True, help_text='Company Telegram contact')

    logo_img = models.ImageField(upload_to='static/img/logo/company/', default='static/img/logo/no-logo.png')

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)

        img = Image.open(self.logo_img)

        if img.height > 250 or img.width > 250:
            new_img_size = 250, 250
            img.thumbnail(new_img_size)
            img.save(self.logo_img.path)

    @property
    def logo_src(self):
        return self.logo_img.url

    def __str__(self):
        return f'{self.name} ({self.city})'

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])


class Project(models.Model):
    name = models.CharField(max_length=128, help_text='Name of the project')
    description = models.TextField(max_length=5000, help_text='Project description')
    company = models.ForeignKey(Company, related_name='projects', on_delete=models.CASCADE)

    logo_img = models.ImageField(upload_to='static/img/logo/company/', default='static/img/logo/no-logo.png')

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

        img = Image.open(self.logo_img)

        if img.height > 250 or img.width > 250:
            new_img_size = 250, 250
            img.thumbnail(new_img_size)
            img.save(self.logo_img.path)

    @property
    def logo_src(self):
        return self.logo_img.url

    def __str__(self):
        return f"{self.name}, ({self.company})"

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])


class Employee(models.Model):
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='companies', on_delete=models.CASCADE)

    ROLES = (('o', 'Owner'), ('e', 'Employee'),)
    role = models.CharField(max_length=1, choices=ROLES, help_text='Role in the company')

    @property
    def role_name(self):
        return dict(Employee.ROLES)[self.role]

    def get_absolute_url(self):
        return reverse('company-employees', args=[str(self.company.id)])

    class Meta:
        ordering = ['-role', 'user']
