from django.db import models
from django.contrib.auth.models import User


class Bank(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    inst_num = models.CharField(max_length=200)
    swift_code = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=200)
    transit_num = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, default='admin@utoronto.ca')
    capacity = models.PositiveIntegerField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='branches')

    def __str__(self):
        return self.name
