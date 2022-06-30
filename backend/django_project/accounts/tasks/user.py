from celery import shared_task
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import logging
logger = logging.getLogger(__name__)
from django.conf import settings

User = get_user_model()



@shared_task(name="create_auth_token", max_retries=3, soft_time_limit=20)
def create_auth_token(accountID=None):
    """ """
    accountUser = User.objects.get(pk=accountID)
    if accountUser:
        token, created = Token.objects.get_or_create(user=accountUser)
        



@shared_task(bind=True, name="clean-users", max_retries=3, soft_time_limit=20)
def clean_temp_users(self):
    """ """
    logger.info("Cleaning test users")
