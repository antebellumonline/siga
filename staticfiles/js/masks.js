/* static/js/masks.js */

document.addEventListener("DOMContentLoaded", function() {
    function formatCPF(value) {
        return value
            .replace(/\D/g, "") // Remove tudo que não for número
            .replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4")
            .slice(0, 14); // Garante que não passe do limite
    }

    function formatCNPJ(value) {
        return value
            .replace(/\D/g, "") // Remove tudo que não for número
            .replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5")
            .slice(0, 18);
    }

    function formatCEP(value) {
        return value
            .replace(/\D/g, "")
            .replace(/(\d{5})(\d{3})/, "$1-$2")
            .slice(0, 9);
    }

    function formatTelefone(value) {
        value = value.replace(/\D/g, ""); // Remove tudo que não for número
        if (value.length <= 10) {
            return value.replace(/(\d{2})(\d{4})(\d{4})/, "($1) $2-$3");
        } else {
            return value.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
        }
    }

    function formatTurmaNome(value) {
        return value.replace(/^([A-Z]{3})(\d{3})(\d{4})(\d{2})(\d{1})$/, "$1$2.$3-$4.$5");
    }

    function applyMask(input, formatter) {
        // Formata ao digitar
        input.addEventListener("input", function() {
            let cursorPosition = input.selectionStart;
            let oldValueLength = input.value.length;

            input.value = formatter(input.value);

            let newValueLength = input.value.length;
            cursorPosition += (newValueLength - oldValueLength);
            input.setSelectionRange(cursorPosition, cursorPosition);
        });

        // Formata ao colar
        input.addEventListener("paste", function(event) {
            event.preventDefault();
            let pastedText = (event.clipboardData || window.clipboardData).getData("text");
            input.value = formatter(pastedText);
        });

        // Aplica a máscara nos valores já preenchidos ao carregar a página
        input.value = formatter(input.value);
    }

    function removeMaskBeforeSubmit() {
        document.querySelectorAll(".cpf-mask, .cnpj-mask, .cep-mask, .telefone-mask, .turma-mask").forEach(input => {
            input.value = input.value.replace(/\D/g, ""); // Remove qualquer formatação antes de enviar
        });
    }

    // Aplica máscara para todos os campos com as classes especificadas
    document.querySelectorAll(".cpf-mask").forEach(input => applyMask(input, formatCPF));
    document.querySelectorAll(".cnpj-mask").forEach(input => applyMask(input, formatCNPJ));
    document.querySelectorAll(".cep-mask").forEach(input => applyMask(input, formatCEP));
    document.querySelectorAll(".telefone-mask").forEach(input => applyMask(input, formatTelefone));

    // Aplica a máscara na listagem das turmas
    document.querySelectorAll(".turma-mask").forEach(input => {
        input.innerText = formatTurmaNome(input.innerText);
    });
    
    // Remove a máscara antes de enviar o formulário
    document.querySelector("form").addEventListener("submit", removeMaskBeforeSubmit);
});
