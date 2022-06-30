
import logging
logger = logging.getLogger(__name__)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.conf import settings
import base64
from django.urls import reverse
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from project.models import BaseModel, StackedModel



class NotificationTokenModel(BaseModel):
    SERIALIZABLES =['id','notification_token']
    READ_ONLY_FIELDS=['id']
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['label']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=['label']
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
 
    TASKS={
        'on_create':["notifications_collection_notificationtokenmodel"],
        'on_save':["stream_live_update_notificationtokenmodel"],
        'on_delete':[]
    }

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,related_name="notificationtokenmodel_criados_por_mim")

    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True ,blank=True, on_delete=models.SET_NULL,related_name="notificationtokenmodel_modificados_por_mim")

    removido_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL,related_name="notificationtokenmodel_removidos_por_mim")

    def get_list_url(self):
        return reverse('notificationtokenmodel-list')

    def get_absolute_url(self):
        return reverse('notificationtokenmodel-detail', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('notificationtokenmodel-delete', args=[str(self.id)])

    def get_detail_url(self):
        return reverse('notificationtokenmodel-detail', args=[str(self.id)])
    
    def get_create_url(self):
        return reverse('notificationtokenmodel-create')

    def get_update_url(self):
        return reverse('notificationtokenmodel-update', args=[str(self.id)])

    notification_token = models.CharField(max_length=512,verbose_name=_("Token de app"))


    @property
    def label(self):
        return self.criado_por.label

    class Meta(BaseModel.Meta):
        verbose_name = _("Token registrado")
        verbose_name_plural = _("Tokens registrados")

    def __str__(self):
        return self.label
