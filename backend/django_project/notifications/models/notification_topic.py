
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



class NotificationTopicModel(BaseModel):
    SERIALIZABLES =['nome_do_topico']
    READ_ONLY_FIELDS=[]
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['nome_do_topico']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
 
    TASKS={
        'on_create':["notifications_collection_notificationtopicmodel"],
        'on_save':["stream_live_update_notificationtopicmodel"],
        'on_delete':[]
    }

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,related_name="notificationtopicmodel_criados_por_mim")

    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True ,blank=True, on_delete=models.SET_NULL,related_name="notificationtopicmodel_modificados_por_mim")

    removido_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL,related_name="notificationtopicmodel_removidos_por_mim")

    def get_list_url(self):
        return reverse('notificationtopicmodel-list')

    def get_absolute_url(self):
        return reverse('notificationtopicmodel-detail', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('notificationtopicmodel-delete', args=[str(self.id)])

    def get_detail_url(self):
        return reverse('notificationtopicmodel-detail', args=[str(self.id)])
    
    def get_create_url(self):
        return reverse('notificationtopicmodel-create')

    def get_update_url(self):
        return reverse('notificationtopicmodel-update', args=[str(self.id)])

    nome_do_topico = models.CharField(max_length=64,verbose_name=_("Nome do tópico"),help_text=_("O nome deve ser uma palavra apenas"))

    icone_do_topico = models.ImageField(upload_to="icones/topicos/",verbose_name=_("Icone do tópico"), help_text=_("Icone será mostrado ao receber a notificação, se suportado pelo celular"))

        

    @property
    def label(self):
        return self.nome_do_topico

    class Meta(BaseModel.Meta):
        verbose_name = _("Topico")
        verbose_name_plural = _("Topicos")

    def __str__(self):
        return self.label
