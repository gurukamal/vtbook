from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from core.choice import *
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

# Create your models here
class CustomUserModel(AbstractUser):
    mobile = models.CharField(max_length=20,blank=True)
    user_type = models.IntegerField(choices=UserType.CHOICES,default=1)
   
    @property
    def name(self):
        return self.get_full_name()