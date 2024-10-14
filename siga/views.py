# siga/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Use com cautela
def delete_item(request, model_name, pk):
    print(f'Requisição recebida: {request.method}, Modelo: {model_name}, PK: {pk}')  # Adicione este print
    if request.method == "POST":
        try:
            Model = apps.get_model('siga', model_name)
            item = get_object_or_404(Model, pk=pk)
            item.delete()
            print(f'Item excluído: {item}')  # Adicione este print
            return JsonResponse({'success': True})
        except LookupError:
            print('Modelo não encontrado.')  # Adicione este print
            return JsonResponse({'success': False, 'error': 'Modelo não encontrado'}, status=404)
    print('Método não permitido.')  # Adicione este print
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
