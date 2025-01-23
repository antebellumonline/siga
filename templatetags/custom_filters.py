from django import template
from urllib.parse import urlencode, parse_qs

register = template.Library()

@register.filter
def remove_page_param(query_params):
    params = parse_qs(query_params)
    params.pop('page', None)  # Remove o parâmetro 'page', se presente
    return urlencode(params, doseq=True)
