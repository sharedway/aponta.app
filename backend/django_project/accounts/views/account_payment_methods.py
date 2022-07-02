"""from django.views.generic.base import TemplateView

[description]
"""
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
import json


class AccountPaymentMethods(TemplateView):
    template_name = "payment_methods.json"
    content_type = "application/json"


    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.user.getPaymentMethods()
        mt = {
            "total": len(m),
            "methods":m
        }
        context.update(
            {"user":self.user,
            "methods": json.dumps(mt)
            })
        return context
