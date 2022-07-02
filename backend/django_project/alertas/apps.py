from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AlertasConfig(AppConfig):
	name = 'alertas'
	verbose_name=_('Alertas')

	def ready(self):
		import alertas.signals
