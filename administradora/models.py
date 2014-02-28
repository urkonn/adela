from django.db import models
from django.contrib.auth.models import User


class Inventory(models.Model):
    data_admin = models.ForeignKey(User)
    data_file = models.FileField(upload_to='inventarios')
    timestamp = models.DateTimeField(auto_now=True)
