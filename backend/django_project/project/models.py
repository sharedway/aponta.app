from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import requests
from django_pandas.managers import DataFrameManager



# Be careful with related_name and related_query_name. Why?
class BaseModel(models.Model):
    AC = "Acre"
    AL = "Alagoas"
    AP = "Amapá"
    AM = "Amazonas"
    BA = "Bahia"
    CE = "Ceará"
    DF = "Distrito Federal"
    ES = "Espírito Santo"
    GO = "Goiás"
    MA = "Maranhão"
    MT = "Mato Grosso"
    MS = "Mato Grosso do Sul"
    MG = "Minas Gerais"
    PA = "Pará"
    PB = "Paraíba"
    PR = "Paraná"
    PE = "Pernambuco"
    PI = "Piauí"
    RJ = "Rio de Janeiro"
    RN = "Rio Grande do Norte"
    RS = "Rio Grande do Sul"
    RO = "Rondônia"
    RR = "Roraima"
    SC = "Santa Catarina"
    SP = "São Paulo"
    SE = "Sergipe"
    TO = "Tocantins"

    ESTADOS_CHOICES = [
        (AC, "Acre"),
        (AL, "Alagoas"),
        (AP, "Amapá"),
        (AM, "Amazonas"),
        (BA, "Bahia"),
        (CE, "Ceará"),
        (DF, "Distrito Federal"),
        (ES, "Espírito Santo"),
        (GO, "Goiás"),
        (MA, "Maranhão"),
        (MT, "Mato Grosso"),
        (MS, "Mato Grosso do Sul"),
        (MG, "Minas Gerais"),
        (PA, "Pará"),
        (PB, "Paraíba"),
        (PR, "Paraná"),
        (PE, "Pernambuco"),
        (PI, "Piauí"),
        (RJ, "Rio de Janeiro"),
        (RN, "Rio Grande do Norte"),
        (RS, "Rio Grande do Sul"),
        (RO, "Rondônia"),
        (RR, "Roraima"),
        (SC, "Santa Catarina"),
        (SP, "São Paulo"),
        (SE, "Sergipe"),
        (TO, "Tocantins"),
    ]

    objects = DataFrameManager()
    created = models.DateTimeField(auto_now=True, verbose_name=_("DT. cadastro"))
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name=_("DT. Atualização")
    )
    isActive = models.BooleanField(default=True, null=True)
    isPublic = models.BooleanField(default=False, null=True)
    isRemoved = models.BooleanField(default=False, null=True)

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    @classmethod
    def propriedades(cls):
        return list(map(lambda f: f.name, cls._meta.fields))

    @classmethod
    def get_or_none(cls, *args, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Exception:
            return None

    def reverse_address_from_postal_code(self,postalcode):
        try:
            url = f"http://45.56.102.198:8181/search.php?postalcode={postalcode}&format=json"
            return requests.get(url, timeout=20).json()        
        except Exception as e:
            print(e.__repr__())
            return [{}]


    class Meta:
        abstract = True
        ordering = ["created"]


class StackedModel(BaseModel):
    stackOrder = models.FloatField(default=100, verbose_name=_("Ordem de exibição"))

    class Meta(BaseModel.Meta):
        abstract = True
        ordering = ["stackOrder"]
