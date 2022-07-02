
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from alertas.models import AlertaModel
from project.admin import project_dashboard_site

@admin.register(AlertaModel)
class AlertaModelAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = AlertaModel.ADMIN_ORDERING
    list_display = AlertaModel.ADMIN_LIST_DISPLAY
    list_filter = AlertaModel.ADMIN_LIST_FILTER
    search_fields = AlertaModel.ADMIN_SEARCH_FILTER
    list_editable = AlertaModel.ADMIN_LIST_EDITABLE
    list_display_links=AlertaModel.ADMIN_DISPLAY_LINKS
    filter_horizontal= AlertaModel.ADMIN_FILTER_HORIZONTAL
    exclude = BaseModelAdmin.exclude + AlertaModel.EXCLUDE_FROM_ADMIN
    actions=['stream_live_update_alertamodel']

    def stream_live_update_alertamodel(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("stream_live_update_alertamodel",[obj.id])
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

    stream_live_update_alertamodel.short_description = _("Send to stream")
    stream_live_update_alertamodel.allowed_permissions = ['stream_live_update_alertamodel']

    def has_stream_live_update_alertamodel_permission(self,request, obj=None):
        return request.user.is_root_user 

    def has_delete_permission(self, request, obj=None):
        return request.user.is_root_user

project_dashboard_site.register(AlertaModel,AlertaModelAdmin)
