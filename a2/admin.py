from django.contrib import admin
from .models import Bank, Branch
from accounts.admin import CustomUserAdmin

# Register your models here.
admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(User, CustomUserAdmin)