from django.contrib import admin
from banks.models import Bank, Branch

# Register your models here.

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'swift_code', 'inst_num', 'description', 'owner')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'transit_num', 'address', 'email', 'capacity', 'last_modified', 'bank')