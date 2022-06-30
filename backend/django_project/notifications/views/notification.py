
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
from notifications.serializers import NotificationModelSerializer
from notifications.models import NotificationModel
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView



class NotificationModelDeleteView(CustomBaseDeleteView):
    template_name = "notificationmodel/notificationmodel_delete.html"
    model = NotificationModel
    success_url = reverse_lazy('notificationmodel-list')
 
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



class NotificationModelCreateView(CustomBaseCreateView):
    template_name = "notificationmodel/notificationmodel_create.html"
    model = NotificationModel
    fields = NotificationModel.CREATE_FIELDS
    success_url = reverse_lazy('notificationmodel-list')
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        if self.next:           
            self.success_url = self.next     
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class NotificationModelUpdateView(CustomBaseUpdateView):
    template_name = "notificationmodel/notificationmodel_update.html"
    model = NotificationModel
    fields = NotificationModel.CREATE_FIELDS
 
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



class NotificationModelDetailView(CustomBaseDetailView):
    template_name = "notificationmodel/notificationmodel_detail.html"
    model = NotificationModel
 
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



class NotificationModelListView(CustomBaseListView):
    template_name = "notificationmodel/notificationmodel_list.html"
    model = NotificationModel
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




class NotificationModelTemplateView(BaseTemplateView):
    template_name = "notificationmodel/notificationmodel_base.html"

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




class NotificationModelViewSet(viewsets.ModelViewSet):
   serializer_class = NotificationModelSerializer
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
       return NotificationModel.objects.filter(isActive=True)
