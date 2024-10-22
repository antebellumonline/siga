// Verificar se a página está pronta
document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada e scripts prontos para uso!");

    // Inicializar o Daterangepicker
    $('#list-daterange').daterangepicker({
        startDate: moment(),
        endDate: moment(),
        timePicker: true,
        timePicker24Hour: true,
        timePickerIncrement: 30,
        locale: {
            format: 'DD/MM/YYYY HH:mm', // Formato da data e hora
            applyLabel: 'Aplicar', // Texto do botão "Aplicar"
            cancelLabel: 'Cancelar', // Texto do botão "Cancelar"
            fromLabel: 'De', // Texto do rótulo "De"
            toLabel: 'Até', // Texto do rótulo "Até"
            weekLabel: 'S', // Rótulo da semana
            customRangeLabel: 'Personalizado', // Texto do rótulo "Personalizado"
            // Nomes dos meses
            monthNames: [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ],
            // Nomes dos dias
            daysOfWeek: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
            firstDay: 1 // Primeiro dia da semana (0 para Domingo, 1 para Segunda)
        },
        opens: 'left' // Abre o calendário à esquerda
    }, function(start, end) {
        // Não usar autoUpdateInput, então só atualize se precisar
        if (start && end) {
            $('#list-daterange').val(start.format('DD/MM/YYYY') + ' - ' + end.format('DD/MM/YYYY'));
        } else {
            $('#list-daterange').val(''); // Limpa o campo se necessário
        }
    });

    // Evento para limpar o campo ao cancelar
    $('#list-daterange').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });

    // Inicializar o Select2
    $.getScript("/static/select2/js/select2.min.js", function() {
        $('#edit-select-cidade, #edit-select-certificador, #edit-select-certificacao, #edit-select-centroProva, #edit-select-aluno, #list-select-cidade, #list-select-certificador, #list-select-certificacao, #list-select-centroProva, #list-select-aluno').select2({
            placeholder: 'Selecione uma Opção',
            allowClear: true
        });
    });

    // Função para ativar/desativar campos com toggleField
    function toggleField(fieldId, isChecked) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.disabled = !isChecked;
            if (!isChecked) {
                field.value = '';
            }
        }
    }

    // Ativação de campos se houver valor inicial ou se a checkbox estiver marcada
    const fieldsToCheck = [
        { checkboxId: 'enable-list-aluno', fieldId: 'list-aluno' },
        { checkboxId: 'enable-list-daterange', fieldId: 'list-daterange' },
        { checkboxId: 'enable-list-centroProva', fieldId: 'list-select-centroProva' },
        { checkboxId: 'enable-list-certificacao', fieldId: 'list-select-certificacao' },
        { checkboxId: 'enable-list-presenca', fieldId: 'list-presenca' },
        { checkboxId: 'enable-list-cancelado', fieldId: 'list-cancelado' }
    ];

    // Desabilitar todos os campos inicialmente
    fieldsToCheck.forEach(item => {
        const field = document.getElementById(item.fieldId);
        if (field) {
            field.disabled = true; // Desabilitar o campo por padrão
        }
    });

    // Verificar o estado das checkboxes e habilitar/desabilitar os campos
    fieldsToCheck.forEach(item => {
        const checkbox = document.getElementById(item.checkboxId);
        if (checkbox) {
            // Configura o campo baseado no estado da checkbox
            toggleField(item.fieldId, checkbox.checked);

            // Adiciona um evento para habilitar/desabilitar conforme a checkbox é clicada
            checkbox.addEventListener('change', function() {
                toggleField(item.fieldId, checkbox.checked);
            });
        }
    });

    // Aplicar máscara para data no formato DD/MM/YYYY
    $('#edit-select-dataExame').mask('00/00/0000 00:00', {placeholder: "dd/mm/aaaa hh:mm"});
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

// -----XXX-----XXX-----XXX-----XXX-----XXX----- //

// ----- Gerenciamento dos Modais e Exclusão via AJAX -----

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
