
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from project.authentication import APITokenAuthentication
from django.views.generic import View
from django.http import JsonResponse
from django.middleware import csrf
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
import re
from django.urls import reverse_lazy
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from project.views import BaseTemplateView
from aplicativos.serializers import AppImagemSerializer
from aplicativos.models import AppImagem
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView



class AppImagemDeleteView(CustomBaseDeleteView):
    template_name = "appimagem/appimagem_delete.html"
    model = AppImagem
    success_url = reverse_lazy('appimagem-list')
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class AppImagemCreateView(CustomBaseCreateView):
    template_name = "appimagem/appimagem_create.html"
    model = AppImagem
    fields = AppImagem.CREATE_FIELDS
    success_url = reverse_lazy('appimagem-list')
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class AppImagemUpdateView(CustomBaseUpdateView):
    template_name = "appimagem/appimagem_update.html"
    model = AppImagem
    fields = AppImagem.CREATE_FIELDS
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class AppImagemDetailView(CustomBaseDetailView):
    template_name = "appimagem/appimagem_detail.html"
    model = AppImagem
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class AppImagemListView(CustomBaseListView):
    template_name = "appimagem/appimagem_list.html"
    model = AppImagem
    paginate_by = 15
    allow_empty = True
    
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)   
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context




class AppImagemTemplateView(BaseTemplateView):
    template_name = "appimagem.html"

    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "body_class":"manager",
            "user":self.user
            })
        context.update(self.common_context())
        return context




class AppImagemViewSet(viewsets.ModelViewSet):
   serializer_class = AppImagemSerializer
   permission_classes = [IsAuthenticated]
   authentication_classes = [SessionAuthentication, APITokenAuthentication]
   parser_classes = [JSONParser]

   def get_serializer_context(self):       
       return {
           "criado_por":self.request.user,         
           "request": self.request,  # request object is passed here
           "format": self.format_kwarg,
           "view": self,
       }

   def get_queryset(self):        
       return AppImagem.objects.filter(isActive=True)
