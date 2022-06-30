from django import template
import hashlib
register = template.Library()

@register.filter(name="email_hash")
def email_hash(email):
    return  hashlib.md5(email.lower().encode()).hexdigest()
