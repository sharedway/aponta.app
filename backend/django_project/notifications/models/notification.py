
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



class NotificationModel(BaseModel):
    SERIALIZABLES =['id','label']
    READ_ONLY_FIELDS=[]
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['titulo','corpo','processing_is_done']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=['processada']
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
 
    TASKS={
        'on_create':["notifications_collection_notificationmodel"],
        'on_save':["stream_live_update_notificationmodel"],
        'on_delete':[]
    }

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,related_name="notificationmodel_criados_por_mim")

    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True ,blank=True, on_delete=models.SET_NULL,related_name="notificationmodel_modificados_por_mim")

    removido_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL,related_name="notificationmodel_removidos_por_mim")

    def get_list_url(self):
        return reverse('notificationmodel-list')

    def get_absolute_url(self):
        return reverse('notificationmodel-detail', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('notificationmodel-delete', args=[str(self.id)])

    def get_detail_url(self):
        return reverse('notificationmodel-detail', args=[str(self.id)])
    
    def get_create_url(self):
        return reverse('notificationmodel-create')

    def get_update_url(self):
        return reverse('notificationmodel-update', args=[str(self.id)])

    # titulo_da_notificacao = models.CharField(max_length=128, verbose_name=_("Titulo da notificação"))

    # mensagem_da_notificacao = models.CharField(max_length=256, verbose_name=_("Mensagem para enviar"), help_text=_("A mensagem deve ser curta, não mais do que 256 carateres, o ideal é até 128"))


    raw_data = models.JSONField(default=dict)

    @property
    def topicos(self):
        return self.raw_data.get('topicos',{'records':[]}).get('records',[])


    @property
    def titulo(self):
        return self.raw_data.get('titulo',"Notificação")
    
    @property
    def corpo(self):
        return self.raw_data.get('corpo',"Notificação")


    
    # topicos = models.ManyToManyField(
    #     "notifications.NotificationTopicModel",
    #     verbose_name=_("Tópicos da notificação"),
    #     help_text=_("Selecione os topicos caso queira enviar para todos"),
    #     blank=True,
    #     related_name="notifications_nesse_topico",        
    # )

    # destinatarios = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     verbose_name=_("Motoristas que devem receber essa notificação"),
    #     related_name="notifications_desse_usuario", 
    #     blank=True
    # )




    processing_started = models.BooleanField(default=False)
    processing_is_done = models.BooleanField(default=False)
    

    @property
    def label(self):
        return self.titulo

    class Meta(BaseModel.Meta):
        verbose_name = _("Notificação")
        verbose_name_plural = _("Notificações")

    def __str__(self):
        return self.label
