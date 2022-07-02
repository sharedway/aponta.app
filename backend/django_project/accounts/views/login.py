from django.views.generic.base import TemplateView


class LoginFormView(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
