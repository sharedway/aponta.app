from django import template
import re
register = template.Library()
tokenValue = re.compile(r"""(?<=<input type="hidden" name="csrfmiddlewaretoken" value=")(.*)(?=">)""", re.IGNORECASE)

@register.filter(name="extract_token")
def extract_token(field):
    results = tokenValue.search(field)
    if results:
        print(results.group(0))
        return "token"
   
    return ""