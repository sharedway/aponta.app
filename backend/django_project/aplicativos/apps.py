from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AplicativosConfig(AppConfig):
	name = 'aplicativos'
	verbose_name=_('Aplicativos')

	def ready(self):
		import aplicativos.signals
