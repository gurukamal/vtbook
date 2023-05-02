from django.db import models
import uuid
from users.models import CustomUserModel as User
from core.choice import *

# Create your models here.

class VehicleRegistration(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vehicle_number = models.CharField(max_length=100, null=True, blank=True)
    driver_name = models.CharField(max_length=100, null=True, blank=True)
    driver_mobile = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.vehicle_number

class CompanyRegistration(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(VehicleRegistration, on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name


class vehicleLedgerLog(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, blank= True, default=None)
    vehicle = models.ForeignKey(VehicleRegistration, on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(CompanyRegistration, on_delete=models.SET_NULL, null=True)
    party_name = models.CharField(max_length=100, null=True, blank=True)
    # total_amount = models.FloatField(null=True, blank=True)
    # recived_amount = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True,default=0)


class PaymentLog(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, blank= True, default=None)
    ledger_log = models.ForeignKey(vehicleLedgerLog, on_delete=models.SET_NULL, null=True)
    type = models.IntegerField(choices=PaymentType.CHOICES,default=1)
    crt_amount = models.FloatField(null= False, blank= False, default=0)
    dbt_amount = models.FloatField(null= False, blank= False, default=0)
    mode = models.IntegerField(choices=PaymentMode.CHOICES,default=1)
    remark = models.TextField(null=True, blank=True, default=None)
    balance = models.FloatField(null= False, blank= False, default=0)

    def save(self, *args, **kwargs):
        if self.type == 1:        #Cedit
            paymentLogObj = PaymentLog.objects.filter(ledger_log = self.ledger_log).last()
            print(paymentLogObj)
            if paymentLogObj:
                last_balance = paymentLogObj.balance
            else:
                last_balance = 0

            self.balance = last_balance+self.crt_amount
            print("Model Override Crdit")
            print(self.ledger_log_id)
            vehicleLedgerLog.objects.filter(id=self.ledger_log_id).update(
                balance = last_balance+self.crt_amount
            )
        elif self.type == 2:      #Debit
            paymentLogObj = PaymentLog.objects.filter(ledger_log = self.ledger_log).last()
            print(paymentLogObj)
            if paymentLogObj:
                last_balance = paymentLogObj.balance
            else:
                last_balance = 0
            
            print(self.dbt_amount)
            print(type(self.dbt_amount))
            print(last_balance)
            print(type(last_balance))

            self.balance = last_balance-self.dbt_amount
            print("Model Override dbit")
            vehicleLedgerLog.objects.filter(id=self.ledger_log_id).update(
                balance = last_balance-self.dbt_amount
            )
        super(PaymentLog, self).save(*args, **kwargs)

# class TxnMode(models.Model):
#     create_at = models.DateTimeField(auto_now_add=True)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     active = models.BooleanField(default=True, null=False, blank=False)
#     txn_mode = models.CharField(null=False, blank= False, max_length=255)