from django import template
import hashlib
register = template.Library()



ICONS = {
    True:"fa-envelope",
    "True":"fa-envelope",
    "False":"id card",
    "id_username":"fa-envelope",
    "id_first_name":"id card",
    "id_last_name":"id card",
    "id_email":"fa-envelope",
    "id_password":"fa-lock",
    "id_password1":"fa-lock",
    "id_password2":"fa-lock",
}

@register.filter(name="get_icon")
def get_icon(ident):

    return ICONS.get(ident,"info")