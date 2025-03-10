/* static/js/masks.js */

// Função para aplicar máscara de CPF
function maskCPF(cpf) {
    return cpf.replace(/(\d{3})(\d)/, '$1.$2')
              .replace(/(\d{3})(\d)/, '$1.$2')
              .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
}

// Função para aplicar máscara de CNPJ
function maskCNPJ(cnpj) {
    return cnpj.replace(/(\d{2})(\d)/, '$1.$2')
               .replace(/(\d{3})(\d)/, '$1.$2')
               .replace(/(\d{3})(\d{1,2})$/, '$1/$2')
               .replace(/(\d{4})(\d{1,2})$/, '$1-$2');
}

// Função para aplicar máscara de Telefone
function maskTelefone(telefone) {
    return telefone.replace(/(\d{2})(\d)/, '($1) $2')
                   .replace(/(\d{4})(\d)/, '$1-$2');
}

// Função para aplicar máscara de Celular
function maskCelular(celular) {
    return celular.replace(/(\d{2})(\d)/, '($1) $2')
                  .replace(/(\d{5})(\d)/, '$1-$2');
}

// Função para aplicar máscara de CEP
function maskCEP(cep) {
    return cep.replace(/(\d{5})(\d)/, '$1-$2');
}

// Função genérica para aplicar a máscara
function applyMask(input, maskFunction) {
    input.addEventListener('input', function() {
        console.log("Input value before mask:", this.value); // Debugging
        this.value = maskFunction(this.value.replace(/\D/g, ''));
        console.log("Input value after mask:", this.value); // Debugging
    });
}

// Inicializa as máscaras
function initMasks() {
    const cpfInputs = document.querySelectorAll('.mask-cpf');
    console.log("CPF Inputs found:", cpfInputs.length); // Debugging
    cpfInputs.forEach(input => applyMask(input, maskCPF));

    const cnpjInputs = document.querySelectorAll('.mask-cnpj');
    cnpjInputs.forEach(input => applyMask(input, maskCNPJ));

    const telefoneInputs = document.querySelectorAll('.mask-telefone');
    telefoneInputs.forEach(input => applyMask(input, maskTelefone));

    const celularInputs = document.querySelectorAll('.mask-celular');
    celularInputs.forEach(input => applyMask(input, maskCelular));

    const cepInputs = document.querySelectorAll('.mask-cep');
    cepInputs.forEach(input => applyMask(input, maskCEP));
}

// Chama a função de inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', initMasks);
