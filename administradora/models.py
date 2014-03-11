from django.db import models
from django.contrib.auth.models import User


class DataAdministrator(models.Model):
    data_admin = models.ForeignKey(User)


class Organization(models.Model):
    data_admin = models.ForeignKey(DataAdministrator)
    organization_name = models.CharField(max_length=50)
    organization_shortname = models.CharField(max_length=10)


class Inventory(models.Model):
    organization = models.ForeignKey(Organization)
    data_file = models.FileField(upload_to='inventarios')
    timestamp = models.DateTimeField(auto_now=True)
