from django import template
register = template.Library()
import datetime
import re
from users.models import CustomUserModel as User
from django.db.models import Q
from django.conf import settings
import datetime
from dashboard.models import PaymentLog,vehicleLedgerLog
from django.db.models import Sum



@register.simple_tag
def caluculate(balance_sheet_id):
    print("Balance Sheet id: ",balance_sheet_id)
    log_list =[]
    vechile_log = vehicleLedgerLog.objects.filter(id=balance_sheet_id).last()
    if vechile_log:
        total_amount = vechile_log.total_amount
        # all_payment_log_obj = PaymentLog.objects.filter(ledger_log = vechile_log.id).aggregate(Sum("amount"))['amount__sum']
        all_payment_log_obj = 0
        if all_payment_log_obj == None:
            all_payment_log_obj = 0
        print(all_payment_log_obj)
        balance = total_amount-all_payment_log_obj
        log_list=[all_payment_log_obj,balance]
    return log_list

@register.simple_tag
def find_remark(balance_sheet_id):
    print("Remark Balance Sheet id: ",balance_sheet_id)
    vechile_log = vehicleLedgerLog.objects.filter(id=balance_sheet_id).last()
    if vechile_log:
        txn_remark = PaymentLog.objects.filter(ledger_log = vechile_log.id).last()
    return txn_remark


