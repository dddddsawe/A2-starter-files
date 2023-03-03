from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Bank(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField()
    inst_num = models.CharField(max_length=120)
    swift_code = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Branch(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=120)
    transit_num = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    email = models.EmailField()
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.bank.name} - {self.name}'
