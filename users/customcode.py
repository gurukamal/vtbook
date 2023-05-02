from django.contrib.auth import get_user_model

def authenticate(username=None, password=None, **kwargs):
    USER_MODEL = get_user_model()

    try:
        userfind = USER_MODEL.objects.get(username=username)

    except USER_MODEL.DoesNotExist:
        return None

    else:
        if userfind.check_password(password):
            return userfind

    return None
