
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
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
from aplicativos.serializers import AplicativoModelSerializer
from aplicativos.models import AplicativoModel
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView



class AplicativoModelDeleteView(CustomBaseDeleteView):
    template_name = "aplicativomodel/aplicativomodel_delete.html"
    model = AplicativoModel
    success_url = reverse_lazy('aplicativomodel-list')
 
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



class AplicativoModelCreateView(CustomBaseCreateView):
    template_name = "aplicativomodel/aplicativomodel_create.html"
    model = AplicativoModel
    fields = AplicativoModel.CREATE_FIELDS
    success_url = reverse_lazy('aplicativomodel-list')
 
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



class AplicativoModelUpdateView(CustomBaseUpdateView):
    template_name = "aplicativomodel/aplicativomodel_update.html"
    model = AplicativoModel
    fields = AplicativoModel.CREATE_FIELDS
 
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



class AplicativoModelDetailView(CustomBaseDetailView):
    template_name = "aplicativomodel/aplicativomodel_detail.html"
    model = AplicativoModel
 
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



class AplicativoModelListView(CustomBaseListView):
    template_name = "aplicativomodel/aplicativomodel_list.html"
    model = AplicativoModel
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




class AplicativoModelTemplateView(BaseTemplateView):
    template_name = "aplicativomodel.html"

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




class AplicativoModelViewSet(viewsets.ModelViewSet):
   serializer_class = AplicativoModelSerializer
   permission_classes = [IsAuthenticatedOrReadOnly]
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
       return AplicativoModel.objects.filter(isActive=True)
