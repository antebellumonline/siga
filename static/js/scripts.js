// Verificar se a página está pronta
document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada e scripts prontos para uso!");

    // Adicionar um evento ao selecionar a quantidade de registros a serem exibidos
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

// Funções para o modal e exclusão via AJAX (que você já possui)

// Obtém o modal
var modal = document.getElementsByClassName("modal-delete")[0];
var cancelBtn = document.getElementsByClassName("btn-cancel")[0];
var span = document.getElementsByClassName("btn-close-modal")[0];

// Quando o usuário clica no botão Excluir, o modal aparece
$(document).on('click', '.btn-delete', function(event) {
    event.preventDefault(); // Impede o link de redirecionar
    var centroProvaPk = $(this).data('pk'); // Obtém o PK do centro de provas
    $('.btn-confirm').data('pk', centroProvaPk); // Armazena o PK no botão de confirmação
    modal.style.display = "block"; // Mostra o modal
});

// Outras funções para modal e AJAX (como você já possui)

// IMPORTAR O JS DO SELECT2
$.getScript("/static/select2/js/select2.min.js", function() {
    $('#select-cidade').select2({
        placeholder: 'Filtrar por Cidade',
        allowClear: true
    });
});
