
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
from aplicativos.models import AplicativoModel
from aplicativos.serializers import AplicativoModelSerializer




@shared_task(name="aplicativos_collection_aplicativomodel", max_retries=2, soft_time_limit=45)
def on_aplicativos_collection_aplicativomodel_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = AplicativoModel.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = AplicativoModelSerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"aplicativos_collection_aplicativomodel", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="stream_live_update_aplicativomodel", max_retries=2, soft_time_limit=45)
def on_stream_live_update_aplicativomodel_task(object_pk):
    instance = AplicativoModel.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = AplicativoModelSerializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"AplicativoModel_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            print(e.__repr__())