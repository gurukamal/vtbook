class UserType(object):
    NONE=0
    ADMIN=1
    CHOICES = (
        (NONE,'None'),
        (ADMIN,'Admin'),
    )


class PaymentType(object):
    NONE=0
    CREDIT=1
    DEBIT=2
    CHOICES = (
        (NONE,'None'),
        (CREDIT,'Credit'),
        (DEBIT,'Debit'),
    )

class PaymentMode(object):
    NONE=0
    CASH=1
    UPI=2
    IMPS=3
    NEFT=4
    RTGS=5
    CHEQUE=6
    CHOICES = (
        (NONE,'None'),
        (CASH,'Cash'),
        (IMPS,'IMPS'),
        (NEFT,'NEFT'),
        (RTGS,'RTGS'),
        (CHEQUE,'Cheque'),
    )