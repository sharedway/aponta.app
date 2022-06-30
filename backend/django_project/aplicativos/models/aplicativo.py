
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



class AplicativoModel(BaseModel):
    SERIALIZABLES =['id','imagens_de_capa','imagem_background_recuperar_senha_imagem_url','imagem_background_login_imagem_url','logotipo_do_app_imagem_url',
    'url_termos_de_uso','url_politica_de_privacidade',
    'url_fale_conosco','url_da_ajuda']
    READ_ONLY_FIELDS=[]
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['label']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= ['imagens_de_capa']
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=['label']
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
 
    TASKS={
        'on_create':["aplicativos_collection_aplicativomodel"],
        'on_save':["stream_live_update_aplicativomodel"],
        'on_delete':[]
    }

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,related_name="aplicativomodel_criados_por_mim")

    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True ,blank=True, on_delete=models.SET_NULL,related_name="aplicativomodel_modificados_por_mim")

    removido_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL,related_name="aplicativomodel_removidos_por_mim")

    def get_list_url(self):
        return reverse('aplicativomodel-list')

    def get_absolute_url(self):
        return reverse('aplicativomodel-detail', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('aplicativomodel-delete', args=[str(self.id)])

    def get_detail_url(self):
        return reverse('aplicativomodel-detail', args=[str(self.id)])
    
    def get_create_url(self):
        return reverse('aplicativomodel-create')

    def get_update_url(self):
        return reverse('aplicativomodel-update', args=[str(self.id)])

    nome_do_app = models.CharField(max_length=512, verbose_name=_("Nome o app"))
    organizacao = models.ForeignKey("organizacoes.Organizacao",
        null=True, blank=True, on_delete=models.SET_NULL,related_name="lista_de_aplicativos_dessa_organizacao")        
    url_termos_de_uso = models.URLField(max_length=512, verbose_name=_("Url dos termos de uso ao app"))
    url_politica_de_privacidade = models.URLField(max_length=512, verbose_name=_("Url da politica de privicade do app"))
    url_fale_conosco = models.URLField(max_length=512, verbose_name=_("Url do SAC"))
    url_da_ajuda = models.URLField(max_length=512, verbose_name=_("Url do FAQ"))

    logotipo_do_app = models.ForeignKey(        
        "aplicativos.AppImagem",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="logotipos",
        help_text=_("Icone do app")        
    )

    @property
    def logotipo_do_app_imagem_url(self):
        return self.logotipo_do_app.imagem_url

    imagem_background_login = models.ForeignKey(
        "aplicativos.AppImagem",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="imagens_de_login",
        help_text=_("Imagem de fundo no login")        
    )
    @property
    def imagem_background_login_imagem_url(self):
        return self.imagem_background_login.imagem_url

    imagem_background_recuperar_senha = models.ForeignKey(
        "aplicativos.AppImagem",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="imagens_de_recuperar_senha",
        help_text=_("Imagem de fundo na recuperação de senha")        
    )

    @property
    def imagem_background_recuperar_senha_imagem_url(self):
        return self.imagem_background_recuperar_senha.imagem_url

    imagens_de_capa = models.ManyToManyField(
        "aplicativos.AppImagem",
        blank=False,
        related_name="apps_usando_essa_imagem"
    )

    @property
    def label(self):
        return self.nome_do_app

    class Meta(BaseModel.Meta):
        verbose_name = _("Aplicativo")
        verbose_name_plural = _("Aplicativo")

    def __str__(self):
        return self.label
