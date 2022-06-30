
import logging
logger = logging.getLogger(__name__)
from celery import shared_task
from django.conf import settings
from django.utils.encoding import smart_str
from PIL import Image, ImageOps, ImageDraw,ImageFont
from io import BytesIO
from django.core.cache import cache
from django.utils.text import slugify
import json
from django.urls import reverse_lazy
import base64
from project.celery_tasks import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import NotificationModel
from notifications.serializers import NotificationModelSerializer
from firebase_admin import messaging
import firebase_admin



@shared_task(name="send_notifications", max_retries=2, soft_time_limit=45)
def on_send_notifications_task():
    notifications = NotificationModel.objects.filter(processing_started=False)

    if notifications.count() >0:

        notification = notifications.first()
        
        if notification:
            notification.processing_started = True
            notification.save()
            app.send_task("send_notifications")
        


            for topico in notification.topicos:
                nome_do_topico = topico.get('nome',None)


                # message = messaging.Message(
                #     topic=topico.nome_do_topico,
                #     notification=messaging.Notification(
                #         title="{title}".format(title=notification.titulo_da_notificacao),
                #         body="{body}".format(body=notification.mensagem_da_notificacao),
                #         image= f"{settings.NOTIFICATIONS_BASE_SITE}/{notification.icone_da_notificacao.url}"
                #     ),
                # )        
                
                # print(messaging.send(message))

            notification.processing_is_done = True
            notification.save()

        
    
    # instance = NotificationModel.get_or_none(pk=object_pk)
    # if instance:
    #     channel_layer = get_channel_layer()        
    #     try:                        
    #         serializador = NotificationModelSerializer(instance)
    #         async_to_sync(channel_layer.group_send)(
    #            f"notifications_collection_notificationmodel", {"type": "group_message", "content": serializador.data}
    #         )
    #     except Exception as e:           
    #         logger.error(e.__repr__())           
    # else:
    #     logger.debug(f"Nao achei {object_pk}")



@shared_task(name="notifications_collection_notificationmodel", max_retries=2, soft_time_limit=45)
def on_notifications_collection_notificationmodel_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = NotificationModel.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = NotificationModelSerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"notifications_collection_notificationmodel", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="stream_live_update_notificationmodel", max_retries=2, soft_time_limit=45)
def on_stream_live_update_notificationmodel_task(object_pk):
    instance = NotificationModel.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = NotificationModelSerializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"NotificationModel_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            print(e.__repr__())