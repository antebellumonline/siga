#!/bin/bash

# Ativar o ambiente virtual
source venv/bin/activate

# Verificar se o ambiente virtual foi ativado com sucesso
if [ $? -ne 0 ]; then
    echo "Falha ao ativar o ambiente virtual. Certifique-se de que o venv esteja configurado corretamente."
    exit 1
fi

echo "Ambiente virtual ativado com sucesso."

# Instalar as dependências existentes no requirements.txt
pip install -r requirements.txt

# Checar se novas dependências foram passadas como argumentos
if [ $# -gt 0 ]; then
    echo "Instalando pacotes adicionais: $@"
    # Instalar novos pacotes que foram passados como argumentos
    pip install "$@"
fi

# Atualizar o arquivo requirements.txt com todas as dependências atuais
pip freeze > requirements.txt

# Confirmar que o arquivo requirements.txt foi atualizado
if [ $? -eq 0 ]; then
    echo "Arquivo requirements.txt atualizado com sucesso."
else
    echo "Erro ao atualizar o requirements.txt."
    exit 1
fi

# Comitar as mudanças no requirements.txt para o repositório
git add requirements.txt
git commit -m "Atualizando requirements.txt durante o deploy"
git push origin main  # Substitua 'main' pelo branch que você está usando

echo "Mudanças enviadas para o repositório."
