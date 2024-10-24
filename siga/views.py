# siga/views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.apps import apps
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, NoReverseMatch

@csrf_exempt  # Use com cautela
def delete_item(request, model_name, pk):
    print(f'Requisição recebida: {request.method}, Modelo: {model_name}, PK: {pk}')  # Adicione este print
    if request.method == "POST":
        try:
            Model = None
            for app in apps.get_app_configs():
                try:
                    Model = app.get_model(model_name)
                    break
                except LookupError:
                    continue
            if not Model:
                print('Modelo não encontrado.')  # Modelo não encontrado
                return JsonResponse({'success': False, 'error': 'Modelo não encontrado'}, status=404)
            
            # Obter o item e excluir
            item = get_object_or_404(Model, pk=pk)
            item.delete()
            print(f'Item excluído: {item}')  # Adicione este print
            
            # Retornar uma resposta de sucesso sem redirecionar
            return JsonResponse({'success': True})
        except Exception as e:
            print(f'Erro ao excluir o item: {e}')
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    print('Método não permitido.')
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)

# ----- View para a Página Inicial do Projeto -----
def home(request):
    return render(request, 'home.html')