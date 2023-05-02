from django.contrib import admin

# Register your models here.
from .models import VehicleRegistration
class VehicleRegistrationAdmin(admin.ModelAdmin):
    list_display=['id','create_at','update_at','active','vehicle_number','driver_name','driver_mobile']
admin.site.register(VehicleRegistration,VehicleRegistrationAdmin)


from .models import CompanyRegistration
class CompanyRegistrationAdmin(admin.ModelAdmin):
    list_display=['id','create_at','update_at','active','company_name','company_address']
admin.site.register(CompanyRegistration,CompanyRegistrationAdmin)


from .models import vehicleLedgerLog
class vehicleLedgerLogAdmin(admin.ModelAdmin):
    list_display=['id','create_at','update_at','active','vehicle','email','mobile','company','party_name']
admin.site.register(vehicleLedgerLog,vehicleLedgerLogAdmin)

# from .models import TxnMode
# class TxnModeAdmin(admin.ModelAdmin):
#     list_display = ['id','create_at','active','txn_mode']
# admin.site.register(TxnMode,TxnModeAdmin)

from .models import PaymentLog
class PaymentLogAdmin(admin.ModelAdmin):
    list_display=['id','create_at','uuid','date','ledger_log','mode']
admin.site.register(PaymentLog,PaymentLogAdmin)