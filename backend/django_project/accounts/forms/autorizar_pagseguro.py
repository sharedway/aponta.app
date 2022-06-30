"""[summary]

[description]
"""
from django.forms import ModelForm
from django import forms


class PagseguroAutorizarForm(forms.Form):
    emailPagseguro = forms.CharField(label="email pagseguro", max_length=100)
    tipoConta = forms.ChoiceField(
        label="email pagseguro",
        choices=[
            ("SELLER", "Vendedor pessoa fisica"),
            ("COMPANY", "Vendedor pessoa juridica"),
        ],
    )
