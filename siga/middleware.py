# siga/middleware.py

"""
Middleware para garantir que o usuário esteja autenticado antes de acessar certas URLs.
"""

"""
Middleware para garantir que o usuário esteja autenticado antes de acessar certas URLs.
"""

from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, reverse, NoReverseMatch

EXEMPT_URLS = [
    settings.LOGIN_URL.lstrip('/'),
    'recuperar-senha/',
    'recuperar-senha/sucesso/',
    'reset/',
    'reset/sucesso/'
]

try:
    EXEMPT_URLS.append(reverse('login'))
except NoReverseMatch:
    pass

try:
    EXEMPT_URLS.append(reverse('logout'))
except NoReverseMatch:
    pass

class LoginRequiredMiddleware:
    """
    Middleware que redireciona usuários não autenticados para a página de login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        if not request.user.is_authenticated and not any(path.startswith(url) for url in EXEMPT_URLS):
            return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response