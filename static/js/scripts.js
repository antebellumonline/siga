// Verificar se a página está pronta
document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada e scripts prontos para uso!");

    // Inicializar o Daterangepicker
    $('#daterange').daterangepicker({
        startDate: moment().subtract(6, 'days'), // Data de início (6 dias atrás)
        endDate: moment(), // Data de fim (hoje)
        locale: {
            format: 'DD/MM/YYYY' // Formato da data
        },
        opens: 'left' // Abre o calendário à esquerda
    }, function(start, end) {
        $('#data_inicio').val(start.format('YYYY-MM-DD')); // Formato YYYY-MM-DD
        $('#data_fim').val(end.format('YYYY-MM-DD')); // Formato YYYY-MM-DD
    });

    // Adicionar evento ao selecionar a quantidade de registros a serem exibidos
    const recordsSelect = document.getElementById('records_per_page');
    if (recordsSelect) {
        recordsSelect.addEventListener('change', function() {
            submitForm();
        });
    }
});


// Função para enviar o formulário com os parâmetros atuais
function submitForm() {
    const form = document.querySelector('.pagination-form'); // Seleciona o formulário
    const searchParams = new URLSearchParams(window.location.search); // Captura os parâmetros da URL
    
    // Adiciona os parâmetros ao formulário
    searchParams.forEach((value, key) => {
        if (key !== 'records_per_page') { // Evita duplicar o parâmetro
            const hiddenField = document.createElement("input");
            hiddenField.type = "hidden";
            hiddenField.name = key;
            hiddenField.value = value;
            form.appendChild(hiddenField);
        }
    });

    form.submit(); // Envia o formulário
}

// Verificar se o jQuery está carregado
$(document).ready(function() {
    // Máscara CPF
    $('#cpf').inputmask('999.999.999-99');
    
    // Máscara CEP
    $('#cep').inputmask('99999-999');
    
    // Máscara para telefones e celulares
    $('.telefone').inputmask({
        mask: ['(99) 9999-9999', '(99) 99999-9999'], 
        keepStatic: true
    });

    // IMPORTAR O JS DO SELECT2
    $.getScript("/static/select2/js/select2.min.js", function() {
        // Inicializar o Select2 no campo 'select' de cidade
        $('select').select2({
            placeholder: 'Selecione uma opção',
            allowClear: true
        });
    });
});

// -----XXX-----XXX-----XXX-----XXX-----XXX----- //

// Funções para os modais e exclusão via AJAX

// Obtém os modais
var modalDelete = document.getElementsByClassName("modal-delete")[0];
var modalFeedback = document.getElementsByClassName("modal-feedback")[0];
var cancelBtn = document.getElementsByClassName("btn-cancel")[0];
var spanDelete = document.getElementsByClassName("btn-close-modal")[0];

// Quando o usuário clica no botão Excluir, o modal de confirmação aparece
$(document).on('click', '.btn-delete', function(event) {
    event.preventDefault(); // Impede o link de redirecionar
    var itemPk = $(this).data('pk'); // Obtém o PK do item a ser excluído
    var modelName = $(this).data('model'); // Obtém o nome do modelo a ser excluído
    var deleteUrl = '/delete/' + modelName + '/' + itemPk + '/'; // Cria a URL de exclusão com base no modelo e PK

    console.log("PK:", itemPk, "Modelo:", modelName, "URL:", deleteUrl); // Adiciona um log para depuração
    $('.btn-confirm').data('pk', itemPk); // Armazena o PK no botão de confirmação
    $('.btn-confirm').data('url', deleteUrl); // Armazena a URL de exclusão no botão de confirmação
    modalDelete.style.display = "block"; // Mostra o modal de confirmação
    modalDelete.style.opacity = 1; // Reseta a opacidade ao mostrar
});

function closeModal(modal) {
    modal.style.opacity = 0; // Inicia a animação de saída
    setTimeout(function() {
        modal.style.display = "none"; // Esconde o modal após a animação
    }, 300); // Tempo da animação
}

// Evento para o botão de cancelamento do modal de confirmação
cancelBtn.onclick = function() {
    closeModal(modalDelete); // Fecha o modal ao clicar no botão cancelar
};

// Evento para o botão de fechar do modal de confirmação
spanDelete.onclick = function() {
    closeModal(modalDelete); // Fecha o modal ao clicar no botão fechar
};

// Fecha o modal de confirmação ao clicar fora dele
window.onclick = function(event) {
    if (event.target === modalDelete) {
        closeModal(modalDelete);
    }
};

// Ação de confirmação da exclusão
$(document).on('click', '.btn-confirm', function() {
    var itemPk = $(this).data('pk'); // Obtém o PK do item a ser excluído
    var deleteUrl = $(this).data('url'); // Usa a URL armazenada no botão de confirmação

    // Realiza a chamada AJAX para excluir o item
    $.ajax({
        url: deleteUrl, // Usa a URL armazenada no botão de confirmação
        type: 'POST', // Usar POST ou DELETE conforme sua configuração
        data: {
            'pk': itemPk,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val() // Captura o token CSRF do formulário
        },
        success: function(response) {
            if (response.success) {
                // Mostra o feedback de sucesso
                showFeedback("Item excluído com sucesso.", true);
            } else {
                // Mostra mensagem de erro
                showFeedback("Erro ao excluir o item: " + response.error, false);
            }
            closeModal(modalDelete);
        },
        error: function(xhr, status, error) {
            // Exibe uma mensagem de erro
            showFeedback("Erro ao excluir o item: " + error, false);
        }
    });
});

// Função para mostrar feedback
function showFeedback(message, isSuccess) {
    modalFeedback.style.display = "block";
    modalFeedback.querySelector(".modal-feedback-message").textContent = message;

    // Exibe a contagem regressiva
    var countdownElement = modalFeedback.querySelector(".countdown-message");
    var countdownTime = 5; // Tempo em segundos para a contagem regressiva
    countdownElement.textContent = "Este pop-up fechará automaticamente em " + countdownTime + " segundos.";

    // Função para atualizar a contagem regressiva
    var countdownInterval = setInterval(function() {
        countdownTime--;
        countdownElement.textContent = "Este pop-up fechará automaticamente em " + countdownTime + " segundos.";
        
        if (countdownTime <= 0) {
            clearInterval(countdownInterval);
            closeModal(modalFeedback); // Fecha o modal após a contagem
            if (isSuccess) {
                // Redireciona para a página anterior após a contagem
                setTimeout(function() {
                    window.history.back(); // Retorna à página anterior
                }, 0); // O redirecionamento imediato após o fechamento
            }
        }
    }, 1000); // Atualiza a cada segundo

    // Se houver um erro, fecha o modal automaticamente após 3 segundos
    if (!isSuccess) {
        // Fecha o modal automaticamente após 3 segundos
        setTimeout(function() {
            clearInterval(countdownInterval); // Limpa o intervalo
            closeModal(modalFeedback); // Fecha o modal de feedback
            closeModal(modalDelete); // Fecha o modal de exclusão também
        }, 5000); // Tempo em milissegundos
    }
}

// IMPORTAR O JS DO SELECT2
$.getScript("/static/select2/js/select2.min.js", function() {
    $('#select-cidade').select2({
        placeholder: 'Selecione a Cidade / UF',
        allowClear: true
    });
});
