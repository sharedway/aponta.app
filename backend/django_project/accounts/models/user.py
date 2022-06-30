from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import json
from functools import reduce
from django.utils.functional import cached_property
import hashlib
from django.conf import settings


class User(AbstractUser):
    USERNAME_VALIDATOR = UnicodeUsernameValidator()
    TASKS={
        'on_create':['create_auth_token'],
        'on_save':[],
        'on_delete':[]
    }
    dateCreated = models.DateTimeField(auto_now=True)
    lastModified = models.DateTimeField(auto_now=True)
    testUser = models.BooleanField(default=False)
    guestUser = models.BooleanField(default=False)
    validEmail = models.BooleanField(default=False)
    isConnected = models.BooleanField(default=False)
    
    email = models.EmailField(unique=True)
    

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "usuário ou email para ser usado no login, usar apenas números, letras e os seguintes caracteres especiais: @/./+/-/_."
        ),
        validators=[USERNAME_VALIDATOR],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )    

    avatar = models.ImageField(upload_to="avatares/",blank=True, null=True, verbose_name=_("Foto do usuario") )
    is_appuser=models.BooleanField(default=False,verbose_name=_("Pode acessar o app"))
    is_root_user=models.BooleanField(default=False,verbose_name=_("SuperAdministrador"))


    android_notification_token = models.CharField(max_length=512,verbose_name=_("Token notificacao Android"))

    ios_notification_token = models.CharField(max_length=512,verbose_name=_("Token notificacao Ios"))


   
    
    @property    
    def chatroomid(self):
        chatroom = self.chatroom.filter(owner=self.id).first()
        if not chatroom:
            return -1
        return chatroom.id
        
    @property
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/icons/user.png"




    @property
    def fullName(self):
        return self.get_full_name()

    @property
    def label(self):
        return self.fullName

    def syncAccount(self):
        pass 
    
    def getSSOToken(self):
        token = default_token_generator.make_token(self)
        uidb64 = urlsafe_base64_encode(str(self.pk).encode())
        return {"token": token, "uidb64": uidb64}    


    def getSessionToken(self):
        token = default_token_generator.make_token(self)
        uidb64 = urlsafe_base64_encode(str(self.pk).encode())
        return {"token": token, "uidb64": uidb64}


    @property
    def servidores(self):
        return []

    @property
    def app_settings(self):
        return {}

    @property
    def authToken(self):
        token = None
        try:
            token = Token.objects.get(user=self)
        except Exception:
            pass

        if not token:
            token = Token.objects.create(user=self)
        return token.key
    @property
    def token(self):
        return self.authToken

    class Meta:
        verbose_name = _("Conta")
        verbose_name_plural = _("Contas")

    def __str__(self):
        return self.fullName
