from django.shortcuts import render,redirect
from .customcode import authenticate
from django.contrib.auth import login as auth_login
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import CustomUserModel as User
from django.contrib.auth import logout as dj_logout

import datetime
import uuid
from django.conf import settings
import random
from django.views.decorators.csrf import csrf_exempt

