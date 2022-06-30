
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from aplicativos.models import AplicativoModel
from project.admin import project_dashboard_site

@admin.register(AplicativoModel)
class AplicativoModelAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = AplicativoModel.ADMIN_ORDERING
    list_display = AplicativoModel.ADMIN_LIST_DISPLAY
    list_filter = AplicativoModel.ADMIN_LIST_FILTER
    search_fields = AplicativoModel.ADMIN_SEARCH_FILTER
    list_editable = AplicativoModel.ADMIN_LIST_EDITABLE
    list_display_links=AplicativoModel.ADMIN_DISPLAY_LINKS
    filter_horizontal= AplicativoModel.ADMIN_FILTER_HORIZONTAL
    exclude = BaseModelAdmin.exclude + AplicativoModel.EXCLUDE_FROM_ADMIN
    actions=['stream_live_update_aplicativomodel']

    def stream_live_update_aplicativomodel(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("stream_live_update_aplicativomodel",[obj.id])
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

    stream_live_update_aplicativomodel.short_description = _("Send to stream")
    stream_live_update_aplicativomodel.allowed_permissions = ['stream_live_update_aplicativomodel']

    def has_stream_live_update_aplicativomodel_permission(self,request, obj=None):
        return request.user.is_root_user 


admin.register(AplicativoModel,AplicativoModelAdmin)
project_dashboard_site.register(AplicativoModel,AplicativoModelAdmin)