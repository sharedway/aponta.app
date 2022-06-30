from django import template
import re
register = template.Library()



@register.filter(name="extract_token")
def extract_token(field):
    tokenValue = re.compile(r"""(?<=<input type="hidden" name="csrfmiddlewaretoken" value=")(.*)(?=">)""", re.IGNORECASE)
    results = tokenValue.search(field)
    if results:
        return results.group(0)
    return field



@register.filter(name="add_attr")
def add_attr(field, css):
    attrs = {}
    definition = css.split(",")

    for d in definition:
        if ":" not in d:
            attrs["class"] = d
        else:
            key, val = d.split(":")
            attrs[key] = val

    return field.as_widget(attrs=attrs)
