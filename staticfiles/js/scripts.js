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
