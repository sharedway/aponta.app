"""
"""
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from kombu import Exchange, Queue, binding

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
redis_host = os.environ.get("REDIS_HOST", default="localhost")
redis_port = os.environ.get("REDIS_PORT", default=6379)
redis_db = os.environ.get("REDIS_DB", default=0)

app = Celery(
    "project",
    broker_url= f"redis://{redis_host}:{redis_port}/{redis_db}",
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(result_expires=3600, enable_utc=True, timezone="America/Sao_Paulo")

# default_exchange = Exchange('default', type='direct')
# media_exchange = Exchange('media', type='direct')

# app.conf.task_queues = (
#     Queue('default', default_exchange, routing_key='default'),
#     Queue('videos', media_exchange, routing_key='media.video'),
#     Queue('images', media_exchange, routing_key='media.image')
# )

app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs): 
    sender.add_periodic_task(
        crontab(minute='*/10'),
        processa_posicoes.s(0),
    )
    app.send_task("processa_posicoes",[0])    
    sender.add_periodic_task(
        crontab(minute='*/1'),
        send_notifications.s(),
    )
    app.send_task("send_notifications")


@app.task
def send_notifications():
    app.send_task("send_notifications")



@app.task
def processa_posicoes(offset):
    app.send_task("processa_posicoes",[offset])