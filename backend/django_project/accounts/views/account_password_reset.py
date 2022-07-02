from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import AccountSerializer
from project.authentication import APITokenAuthentication
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.middleware import csrf
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
import re
from django.urls import reverse_lazy

from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.views import (
   PasswordResetView,
)
from django.contrib.auth.tokens import default_token_generator


from django.contrib.auth import authenticate

isValidEmail = re.compile(r"[\w\.-]+@[\w\.-]+(\.[\w]+)+")

User = get_user_model()


class AccountPasswordResetView(View):
    def get(self, request):
        return JsonResponse({"csrftoken": "%s" % csrf.get_token(request)}, status=200)

    def post(self, request):        
        form = PasswordResetForm(json.loads(request.body))
        if form.is_valid():
            print("Recuperando senha")
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'email_template_name': 'registration/password_reset_email.html',
                'subject_template_name': 'registration/password_reset_subject.txt',
                'request': request,
                'html_email_template_name': 'registration/password_reset_email.html',
            }
            form.save(**opts)
        else:
            print(request.body)
            print("Recuperando senha com erro")
        return JsonResponse({"csrftoken": "%s" % csrf.get_token(request)}, status=200)



