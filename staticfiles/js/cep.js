/* static/js/cep.js */
function buscaEndereco() {
    var cep = document.getElementById("cep").value;
    fetch(`/apis/buscacep/${cep}/`)
        .then(response => response.json())
        .then(data => {
            if (data.ibge) {
                document.getElementById("logradouro").value = data.logradouro;
                document.getElementById("bairro").value = data.bairro;
                $('#select-cidade').val(data.ibge).trigger('change');
            } else {
                alert("CEP não encontrado!");
            }
        })
        .catch(error => console.error("Erro na busca do CEP:", error));
}

document.addEventListener("DOMContentLoaded", function() {
    const cepInput = document.getElementById('cep');
    if (cepInput) {
        cepInput.addEventListener('blur', buscaEndereco);
    }
});
