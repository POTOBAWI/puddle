from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    """Renvoie True si la chaîne se termine par le suffixe donné"""
    if isinstance(value, str):
        return value.lower().endswith(suffix.lower())
    return False
