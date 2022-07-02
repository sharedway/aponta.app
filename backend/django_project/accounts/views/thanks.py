from django.views.generic.base import TemplateView


class ContactThanks(TemplateView):
    template_name = "thanks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
