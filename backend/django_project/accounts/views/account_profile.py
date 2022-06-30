"""from django.views.generic.base import TemplateView

[description]
"""
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.middleware import csrf
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView
from project.celery_tasks import app
from project.views import BaseTemplateView


class AccountProfile(BaseTemplateView):
    template_name = "profile.html"


    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user        
        return super().dispatch(*args, **kwargs)



    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({"csrftoken":csrf.get_token(self.request),"setup_intent":json.dumps(dict(self.setup_intent.to_dict_recursive())),
    #         "user": self.user, "publicKey": self.stripeSettings.publicKey})
    #     return context


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
