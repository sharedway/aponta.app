from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DatavaultConfig(AppConfig):
	name = 'datavault'
	verbose_name=_('Datavault')

	def ready(self):
		import datavault.signals
