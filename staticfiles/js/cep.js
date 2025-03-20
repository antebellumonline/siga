/* static/js/cep.js */
function buscaEndereco(event) {
    var cepInput = event.target;
    var form = cepInput.closest('form'); // Identifica o formulário mais próximo

    if (!form) return; // Se não estiver dentro de um formulário, sai

    var cep = cepInput.value.trim();

    if (!cep) return;

    fetch(`/apis/buscacep/${cep}/`)
        .then(response => response.json())
        .then(data => {
            if (data.ibge) {
                form.querySelector(".logradouro-input").value = data.logradouro || "";
                form.querySelector(".bairro-input").value = data.bairro || "";
                $(form.querySelector(".cidade-input")).val(data.ibge).trigger('change');
            } else {
                alert("CEP não encontrado!");
            }
        })
        .catch(error => console.error("Erro na busca do CEP:", error));
}

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".cep-input").forEach(input => {
        input.addEventListener("blur", buscaEndereco);
    });
});
