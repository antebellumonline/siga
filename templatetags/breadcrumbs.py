# templatetags/breadcrumbs.py

from django import template
from django.urls import resolve, reverse, Resolver404
from django.utils.html import format_html

register = template.Library()

@register.simple_tag(takes_context=True)
def generate_breadcrumbs(context):
    """
    Gera breadcrumbs dinâmicos com base na estrutura das URLs.
    """
    request = context['request']
    path = request.path

    try:
        resolver_match = resolve(path)
        print(f"Resolver match: {resolver_match}")
    except Resolver404:
        return ''

    breadcrumbs = []
    url_accumulator = ''

    parts = path.strip('/').split('/')
    print(f"URL parts: {parts}")

    for index, part in enumerate(parts):
        url_accumulator = '/' + '/'.join(parts[:index + 1])  # Mantém a hierarquia correta
        try:
            match = resolve(url_accumulator)
            print(f"Match for {url_accumulator}: {match}")
            if match.url_name:
                nome_formatado = match.url_name.replace('_', ' ').title()
                url_final = reverse(match.view_name, kwargs=match.kwargs)
                if (url_final, nome_formatado) not in breadcrumbs:
                    breadcrumbs.append((url_final, nome_formatado))
        except Resolver404:
            print(f"Resolver404 for accumulated URL: {url_accumulator}")
            continue

    print(f"Generated breadcrumbs: {breadcrumbs}")

    breadcrumb_html = '<nav aria-label="breadcrumb"><ol class="breadcrumb">'
    breadcrumb_html += f'<li class="breadcrumb-item"><a href="{reverse("home")}"><i class="fa fa-home"></i> Home</a></li>'

    for crumb in breadcrumbs:
        breadcrumb_html += f'<li class="breadcrumb-item"><a href="{crumb[0]}">{crumb[1]}</a></li>'

    breadcrumb_html += '</ol></nav>'
    
    return format_html(breadcrumb_html)