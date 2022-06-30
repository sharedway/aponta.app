
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from aplicativos.models import AppImagem
from project.admin import project_dashboard_site

@admin.register(AppImagem)
class AppImagemAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = AppImagem.ADMIN_ORDERING
    list_display = AppImagem.ADMIN_LIST_DISPLAY+['img_url']
    list_filter = AppImagem.ADMIN_LIST_FILTER
    search_fields = AppImagem.ADMIN_SEARCH_FILTER
    list_editable = AppImagem.ADMIN_LIST_EDITABLE
    list_display_links=AppImagem.ADMIN_DISPLAY_LINKS
    filter_horizontal= AppImagem.ADMIN_FILTER_HORIZONTAL
    exclude = BaseModelAdmin.exclude + AppImagem.EXCLUDE_FROM_ADMIN
    actions=['stream_live_update_appimagem']

    def img_url(self, obj):  # receives the instance as an argument
        return mark_safe(
            '<img width=96px src="{url}" />'.format(
                url=obj.imagem.url,
            )
        )
    img_url.allow_tags = True
    img_url.short_description = "Original"


    def stream_live_update_appimagem(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("stream_live_update_appimagem",[obj.id])
            except Exception as e:
                self.message_user(
                    request,
                    f"{obj.label}: {e.__repr__()}",
                    messages.ERROR,
                )
            else:
                self.message_user(
                    request,
                    "{label}: enviado para a fila de processamento".format(label=obj),
                    messages.SUCCESS,
                )

    stream_live_update_appimagem.short_description = _("Send to stream")
    stream_live_update_appimagem.allowed_permissions = ['stream_live_update_appimagem']

    def has_stream_live_update_appimagem_permission(self,request, obj=None):
        return request.user.is_root_user 



project_dashboard_site.register(AppImagem,AppImagemAdmin)