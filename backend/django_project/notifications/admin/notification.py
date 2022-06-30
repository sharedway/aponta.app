
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from notifications.models import NotificationModel


@admin.register(NotificationModel)
class NotificationModelAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = NotificationModel.ADMIN_ORDERING
    list_display = NotificationModel.ADMIN_LIST_DISPLAY
    list_filter = NotificationModel.ADMIN_LIST_FILTER
    search_fields = NotificationModel.ADMIN_SEARCH_FILTER
    list_editable = NotificationModel.ADMIN_LIST_EDITABLE
    list_display_links=NotificationModel.ADMIN_DISPLAY_LINKS
    filter_horizontal= NotificationModel.ADMIN_FILTER_HORIZONTAL
    exclude = BaseModelAdmin.exclude + NotificationModel.EXCLUDE_FROM_ADMIN
    actions=['stream_live_update_notificationmodel']

    def stream_live_update_notificationmodel(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("stream_live_update_notificationmodel",[obj.id])
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

    stream_live_update_notificationmodel.short_description = _("Send to stream")
    stream_live_update_notificationmodel.allowed_permissions = ['stream_live_update_notificationmodel']

    def has_stream_live_update_notificationmodel_permission(self,request, obj=None):
        return request.user.is_superuser  



    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):	        
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
