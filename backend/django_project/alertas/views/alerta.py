
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
from alertas.serializers import AlertaModelSerializer
from alertas.models import AlertaModel
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView



class AlertaModelDeleteView(CustomBaseDeleteView):
    template_name = "alertamodel/web_templates/v1/alertamodel_delete.html"
    model = AlertaModel
    success_url = reverse_lazy('alertamodel-list')




class AlertaModelCreateView(CustomBaseCreateView):
    template_name = "alertamodel/web_templates/v1/alertamodel_create.html"
    model = AlertaModel
    fields = AlertaModel.CREATE_FIELDS
    success_url = reverse_lazy('alertamodel-list')
 




class AlertaModelUpdateView(CustomBaseUpdateView):
    template_name = "alertamodel/web_templates/v1/alertamodel_update.html"
    model = AlertaModel
    fields = AlertaModel.CREATE_FIELDS
 




class AlertaModelDetailView(CustomBaseDetailView):
    template_name = "alertamodel/web_templates/v1/alertamodel_detail.html"
    model = AlertaModel
 



class AlertaModelListView(CustomBaseListView):
    template_name = "alertamodel/web_templates/v1/alertamodel_list.html"
    model = AlertaModel
    paginate_by = 15
    allow_empty = True
    




class AlertaModelTemplateView(BaseTemplateView):
    template_name = "alertamodel/web_templates/v1/alertamodel_base.html"






class AlertaModelViewSet(viewsets.ModelViewSet):
   serializer_class = AlertaModelSerializer
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
       return AlertaModel.objects.filter(isActive=True)
