# siga/middleware.py

"""
Middleware para garantir que o usuário esteja autenticado antes de acessar certas URLs.
"""

from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch

EXEMPT_URLS = []

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
        if not request.user.is_authenticated and request.path not in EXEMPT_URLS:
            return redirect('login')
        response = self.get_response(request)
        return response
