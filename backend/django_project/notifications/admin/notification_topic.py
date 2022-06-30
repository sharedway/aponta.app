
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from notifications.models import NotificationTopicModel


@admin.register(NotificationTopicModel)
class NotificationTopicModelAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = NotificationTopicModel.ADMIN_ORDERING
    list_display = NotificationTopicModel.ADMIN_LIST_DISPLAY+['img_url']
    list_filter = NotificationTopicModel.ADMIN_LIST_FILTER
    search_fields = NotificationTopicModel.ADMIN_SEARCH_FILTER
    list_editable = NotificationTopicModel.ADMIN_LIST_EDITABLE
    list_display_links=NotificationTopicModel.ADMIN_DISPLAY_LINKS
    filter_horizontal= NotificationTopicModel.ADMIN_FILTER_HORIZONTAL
    exclude = BaseModelAdmin.exclude + NotificationTopicModel.EXCLUDE_FROM_ADMIN
    actions=['stream_live_update_notificationtopicmodel']

    def img_url(self, obj):  # receives the instance as an argument
        return mark_safe(
            '<img width=96px src="{url}" />'.format(
                url=obj.icone_do_topico.url,
            )
        )
    img_url.allow_tags = True
    img_url.short_description = "Icone"

    def stream_live_update_notificationtopicmodel(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("stream_live_update_notificationtopicmodel",[obj.id])
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

    stream_live_update_notificationtopicmodel.short_description = _("Send to stream")
    stream_live_update_notificationtopicmodel.allowed_permissions = ['stream_live_update_notificationtopicmodel']

    def has_stream_live_update_notificationtopicmodel_permission(self,request, obj=None):
        return request.user.is_superuser  



    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):	        
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
