"""[summary]

[description]
"""

from django.views.generic.base import TemplateView
from accounts.forms import UserCreateForm
from django.views.generic.edit import FormView
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class AccountSignin(FormView):
    template_name = "account_signin.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("account-profile")
    user_exist_url = reverse_lazy("password_reset")
    subject_template_name = ("signin_subject.txt",)
    email_template_name = ("signin_email.html",)

    def form_valid(self, form, **kwargs):
        context = super().get_context_data(**kwargs)
        if len(list(form.get_users())) < 1:
            form.save(request=self.request)
        else:
            return HttpResponseRedirect(self.user_exist_url)

        return super().form_valid(form)
