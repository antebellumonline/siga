/* static/js/cnpj.js */
function buscaCNPJ(event) {
    var cnpjInput = event.target;
    var form = cnpjInput.closest('form'); // Encontra o formulário mais próximo

    if (!form) return; // Se não estiver dentro de um formulário, sai

    var cnpj = cnpjInput.value.replace(/\D/g, ''); // Remove caracteres não numéricos

    if (!cnpj) return;

    fetch(`/apis/buscacnpj/${cnpj}/`)
        .then(response => response.json())
        .then(data => {
            if (!data.erro) {
                let razaoSocial = form.querySelector(".razaoSocial-input");
                let fantasia = form.querySelector(".fantasia-input");
                let cep = form.querySelector(".cep-input");
                let logradouro = form.querySelector(".logradouro-input");
                let numero = form.querySelector(".endereco-numero-input");
                let complemento = form.querySelector(".complemento-input");
                let bairro = form.querySelector(".bairro-input");
                let cidade = form.querySelector(".cidade-input");

                if (razaoSocial) razaoSocial.value = data.razaoSocial || "";
                if (fantasia) fantasia.value = data.fantasia || "";
                if (cep) cep.value = data.cep || "";
                if (logradouro) logradouro.value = data.endereco || "";
                if (numero) numero.value = data.numero || "";
                if (complemento) complemento.value = data.complemento || "";
                if (bairro) bairro.value = data.bairro || "";
                if (cidade) $(cidade).val(data.ibge).trigger('change'); // IBGE no select
            } else {
                alert("CNPJ não encontrado!");
            }
        })
        .catch(error => console.error("Erro na busca do CNPJ:", error));
}

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".taxId-input").forEach(input => {
        input.addEventListener("blur", buscaCNPJ);
    });
});
