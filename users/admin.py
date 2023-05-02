from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display =['id','name','email','mobile']
    
    def save_model(self, request, obj, form, change):
        # Override this to set the password to the value in the field if it's
        # changed.
        if obj.pk:
            orig_obj = CustomUserModel.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(CustomUserModel,UserAdmin)
