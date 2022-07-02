
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_init,
    post_init,
    pre_delete,
    post_delete,
    m2m_changed,
)

import hashlib
from django.dispatch import receiver
from django.conf import settings
from project.celery_tasks import app
from alertas.models import AlertaModel


@receiver(post_save, sender=AlertaModel)
def PostSaveAlertaModelSignals(
    sender, instance, created, using, update_fields, *args, **kwargs
):
    if True in [created]:
        for task in AlertaModel.TASKS.get('on_create',[]):
            app.send_task(task, [instance.id])
    else:
        for task in AlertaModel.TASKS.get('on_save',[]):
            app.send_task(task, [instance.id])