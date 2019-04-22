from django.contrib import admin
from .models import *

def active_deal(self, request, queryset):
    row_updated = queryset.update(status = True)
    if row_updated ==1:
        message_bit = '1 record is updated successfully'
    elif row_updated >1:
        message_bit = row_updated %' record is updated successfully'
    else:
        message_bit = 'Update error!!!'
    self.message_user(request, message_bit)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'branch_admin', 'branch_address')


class StoreAdmin(admin.ModelAdmin):
    list_display = ('branch', 'good', 'amount')
    list_filter = ('branch', 'good')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('time_deal', 'good', 'amount', 'tyles', 'ware_source', 'ware_des', 'status')
    list_filter = ('tyles', 'ware_source', 'ware_des', 'status')
    actions = [active_deal]
    # form = HistoryformAdmin

# Register your models here.
admin.site.register(Goods)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Warehouse, StoreAdmin)
admin.site.register(History_deal, HistoryAdmin)
