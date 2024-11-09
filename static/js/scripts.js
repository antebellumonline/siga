// Verificar se a página está pronta
document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada e scripts prontos para uso!");

    // Inicializar o Daterangepicker
    $('.daterange').daterangepicker({
        startDate: moment(),
        endDate: moment(),
        locale: {
            format: 'DD/MM/YYYY', // Formato da data e hora
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
            $('.daterange').val(start.format('DD/MM/YYYY') + ' - ' + end.format('DD/MM/YYYY'));
        } else {
            $('.daterange').val(''); // Limpa o campo se necessário
        }
    });

    // Evento para limpar o campo ao cancelar
    $('.daterange').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });

    // Inicializar o Select2 para todos os elementos com a classe "select2"
    $.getScript("/static/select2/js/select2.min.js", function() {
        $('.select2').select2({
            placeholder: 'Selecione uma Opção',
            allowClear: true
        });
    });

    // Adicionar evento de blur ao campo de CEP
    const cepInput = document.getElementById('cep');
    if (cepInput) {
        console.log("Campo CEP encontrado, adicionando evento blur");
        cepInput.addEventListener('blur', function() {
            console.log("Evento blur acionado!");
            buscaEndereco();
        });
    } else {
        console.log("Campo CEP não encontrado");
    }

    // Seleciona todos os checkboxes com o atributo data-target
    const checkboxes = document.querySelectorAll('input[type="checkbox"][data-target]');

    // Função para ativar/desativar campos
    const toggleField = (field, isChecked) => {
        if (field) {
            field.disabled = !isChecked;
            if (!isChecked) {
                field.value = '';
            }
        }
    };

    // Inicializa o estado dos campos e configura os eventos
    checkboxes.forEach(checkbox => {
        const targetField = document.getElementById(checkbox.dataset.target);
        if (targetField) {
            // Configura o campo inicialmente
            toggleField(targetField, checkbox.checked);

            // Adiciona o evento de mudança para o checkbox
            checkbox.addEventListener('change', function() {
                toggleField(targetField, checkbox.checked);
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

// Função para buscar o endereço pelo CEP
function buscaEndereco() {
    var cep = document.getElementById("cep").value;
    console.log("CEP digitado:", cep);
    fetch(`/apis/buscacep/${cep}/`)
        .then(response => {
            console.log("Resposta da API:", response);
            return response.json();
        })
        .then(data => {
            console.log("Dados recebidos:", data);
            if (data.ibge) {
                document.getElementById("logradouro").value = data.logradouro;
                document.getElementById("bairro").value = data.bairro;
                const selectCidade = $('#select-cidade');
                console.log("Código IBGE recebido:", data.ibge);
                selectCidade.val(data.ibge).trigger('change');
            } else {
                alert("CEP não encontrado!");
            }
        })
        .catch(error => {
            console.error("Erro na busca do CEP:", error);
        });
}

// -----XXX-----XXX-----XXX-----XXX-----XXX----- //

// ----- Gerenciamento dos Modais e Exclusão via AJAX -----

// Obtém os modais
var modalDelete = document.getElementsByClassName("modal-delete")[0];
var modalFeedback = document.getElementsByClassName("modal-feedback")[0];
var cancelBtn = document.getElementsByClassName("btn-cancel")[0];
var spanDelete = document.getElementsByClassName("btn-close-modal")[0];

// Função para abrir um modal
function openModal(modal) {
    console.log('Abrindo modal:', modal); // Log
    modal.style.display = "block";
    requestAnimationFrame(function() {
        modal.style.opacity = "1";
    });
}

// Função para fechar um modal
function closeModal(modal) {
    console.log('Fechando modal:', modal); // Log
    modal.style.opacity = "0";
    setTimeout(function() {
        modal.style.display = "none";
    }, 300);
}

// Quando o usuário clica no botão Excluir
$(document).on('click', '.btn-delete', function(event) {
    console.log('Botão Excluir clicado'); // Log
    event.preventDefault();
    var itemPk = $(this).data('pk');
    var modelName = $(this).data('model');
    var deleteUrl = '/delete/' + modelName + '/' + itemPk + '/';

    console.log("PK:", itemPk, "Modelo:", modelName, "URL:", deleteUrl);
    $('.btn-confirm').data('pk', itemPk);
    $('.btn-confirm').data('url', deleteUrl);
    openModal(modalDelete);
});

// Evento para o botão de cancelamento do modal de confirmação
cancelBtn.onclick = function() {
    closeModal(modalDelete);
};

// Evento para o botão de fechar do modal de confirmação
spanDelete.onclick = function() {
    closeModal(modalDelete);
};

// Fecha o modal de confirmação ao clicar fora dele
window.onclick = function(event) {
    if (event.target === modalDelete) {
        closeModal(modalDelete);
    }
};

// Ação de confirmação da exclusão
$(document).on('click', '.btn-confirm', function() {
    console.log('Botão Confirmar clicado'); // Log
    var itemPk = $(this).data('pk');
    var deleteUrl = $(this).data('url');

    $.ajax({
        url: deleteUrl,
        type: 'POST',
        data: {
            'pk': itemPk,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
            console.log('Resposta do servidor:', response); // Log
            if (response.success) {
                showFeedback("Item excluído com sucesso.", true);
            } else {
                showFeedback("Erro ao excluir o item: " + response.error, false);
            }
            closeModal(modalDelete);
        },
        error: function(xhr, status, error) {
            console.error('Erro na chamada AJAX:', error); // Log
            showFeedback("Erro ao excluir o item: " + error, false);
        }
    });
});

// Função para mostrar feedback
function showFeedback(message, isSuccess) {
    modalFeedback.style.display = "block";
    modalFeedback.querySelector(".modal-feedback-message").textContent = message;

    var countdownElement = modalFeedback.querySelector(".countdown-message");
    var countdownTime = 5;
    countdownElement.textContent = "Este pop-up fechará automaticamente em " + countdownTime + " segundos.";

    var countdownInterval = setInterval(function() {
        countdownTime--;
        countdownElement.textContent = "Este pop-up fechará automaticamente em " + countdownTime + " segundos.";
        
        if (countdownTime <= 0) {
            clearInterval(countdownInterval);
            closeModal(modalFeedback);
            if (isSuccess) {
                setTimeout(function() {
                    window.history.back();
                }, 0);
            }
        }
    }, 1000);

    if (!isSuccess) {
        setTimeout(function() {
            clearInterval(countdownInterval);
            closeModal(modalFeedback);
            closeModal(modalDelete);
        }, 5000);
    }
}
