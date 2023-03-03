from django.contrib import admin
from banks.models import Bank, Branch

# Register your models here.


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'swift_code', 'inst_num', 'description', 'owner')


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank', 'transit_num', 'address', 'email', 'capacity', 'last_modified_display')

    def last_modified_display(self, obj):
        return obj.last_modified
    last_modified_display.admin_order_field = 'last_modified'
    last_modified_display.short_description = 'Last Modified'
