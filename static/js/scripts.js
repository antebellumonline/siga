// Exemplo de script JavaScript
document.addEventListener("DOMContentLoaded", function() {
    console.log("Página carregada e scripts prontos para uso!");

    // Você pode adicionar interatividade aqui, por exemplo:
    // document.querySelector("button").addEventListener("click", function() {
    //     alert("Botão clicado!");
    // });
});

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
});

// -----XXX-----XXX-----XXX-----XXX-----XXX----- //

// Obtém o modal
var modal = document.getElementsByClassName("modal-delete")[0];

// Obtém o botão de cancelar
var cancelBtn = document.getElementsByClassName("btn-cancel")[0];

// Obtém o elemento <span> que fecha o modal
var span = document.getElementsByClassName("btn-close-modal")[0];

// Quando o usuário clica no botão Excluir, o modal aparece
$(document).on('click', '.btn-delete', function(event) {
    event.preventDefault(); // Impede o link de redirecionar
    var centroProvaPk = $(this).data('pk'); // Obtém o PK do centro de provas
    $('.btn-confirm').data('pk', centroProvaPk); // Armazena o PK no botão de confirmação
    modal.style.display = "block"; // Mostra o modal
});

// Quando o usuário clica no botão Cancelar, o modal desaparece
cancelBtn.onclick = function() {
    modal.style.display = "none";
}

// Quando o usuário clica no <span> (x), o modal desaparece
span.onclick = function() {
    modal.style.display = "none";
}

// Quando o usuário clica fora do modal, ele desaparece
window.onclick = function(event) {
    if (event.target === modal) { // Verifica se o clique foi fora do modal
        modal.style.display = "none";
    }
}

// Confirmar exclusão com AJAX
$('.btn-confirm').click(function() {
    var centroProvaPk = $(this).data('pk'); // Recupera o PK armazenado
    var url = "/centroProva/delete/" + centroProvaPk + "/"; // Constrói a URL para exclusão

    $.ajax({
        url: url,
        type: "POST",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}', // Token CSRF para segurança
        },
        success: function(response) {
            modal.style.display = "none"; // Oculta o modal
            $('.modal-feedback-message').text('Centro de Provas excluído com sucesso.');
            $('.modal-feedback').show(); // Mostra o modal de feedback
        },
        error: function(xhr, errmsg, err) {
            modal.style.display = "none"; // Oculta o modal
            $('.modal-feedback-message').text('Erro ao excluir o Centro de Provas.');
            $('.modal-feedback').show(); // Mostra o modal de feedback
        }
    });
});

// Fechar o modal de feedback
$('.btn-close').click(function() {
    $('.modal-feedback').hide();
    window.location.href = $(this).data('url'); // Redireciona para a lista após fechar o modal
});
