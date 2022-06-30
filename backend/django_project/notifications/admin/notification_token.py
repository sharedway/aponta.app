
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from notifications.models import NotificationTokenModel


@admin.register(NotificationTokenModel)
class NotificationTokenModelAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = NotificationTokenModel.ADMIN_ORDERING
    list_display = NotificationTokenModel.ADMIN_LIST_DISPLAY
    list_filter = NotificationTokenModel.ADMIN_LIST_FILTER
    search_fields = NotificationTokenModel.ADMIN_SEARCH_FILTER
    list_editable = NotificationTokenModel.ADMIN_LIST_EDITABLE
    list_display_links=NotificationTokenModel.ADMIN_DISPLAY_LINKS
    filter_horizontal= NotificationTokenModel.ADMIN_FILTER_HORIZONTAL
    exclude = BaseModelAdmin.exclude + NotificationTokenModel.EXCLUDE_FROM_ADMIN
    actions=['stream_live_update_notificationtokenmodel']

    def stream_live_update_notificationtokenmodel(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("stream_live_update_notificationtokenmodel",[obj.id])
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

    stream_live_update_notificationtokenmodel.short_description = _("Send to stream")
    stream_live_update_notificationtokenmodel.allowed_permissions = ['stream_live_update_notificationtokenmodel']

    def has_stream_live_update_notificationtokenmodel_permission(self,request, obj=None):
        return request.user.is_superuser  



    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):	        
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
