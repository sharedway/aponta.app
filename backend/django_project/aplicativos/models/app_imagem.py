
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



class AppImagem(BaseModel):
    SERIALIZABLES =['imagem_url','descricao_da_imagem']
    READ_ONLY_FIELDS=[]
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['id','label']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=['label']
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
 
    TASKS={
        'on_create':["aplicativos_collection_appimagem"],
        'on_save':["stream_live_update_appimagem"],
        'on_delete':[]
    }

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,related_name="appimagem_criados_por_mim")

    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True ,blank=True, on_delete=models.SET_NULL,related_name="appimagem_modificados_por_mim")

    removido_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL,related_name="appimagem_removidos_por_mim")

    def get_list_url(self):
        return reverse('appimagem-list')

    def get_absolute_url(self):
        return reverse('appimagem-detail', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('appimagem-delete', args=[str(self.id)])

    def get_detail_url(self):
        return reverse('appimagem-detail', args=[str(self.id)])
    
    def get_create_url(self):
        return reverse('appimagem-create')

    def get_update_url(self):
        return reverse('appimagem-update', args=[str(self.id)])


    descricao_da_imagem  = models.CharField(max_length=126,verbose_name=_("Descrição da imagem"))  
    imagem = models.ImageField(upload_to="apps/imagens/")

    @property
    def imagem_url(self):
        return self.imagem.url

    @property
    def label(self):
        return self.descricao_da_imagem

    class Meta(BaseModel.Meta):
        verbose_name = _("Imagem")
        verbose_name_plural = _("Imagem")

    def __str__(self):
        return self.label
