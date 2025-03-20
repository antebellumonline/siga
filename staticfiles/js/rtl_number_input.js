/* static/js/rtl_number_input.js */

document.addEventListener('DOMContentLoaded', function() {
    function formatNumberInput(input, onBlur = false) {
        let value = input.value.replace(/\D/g, ''); // Remove tudo que não for número

        if (value.length === 0) {
            if (onBlur) {
                input.value = '';
            }
            return;
        }

        while (value.length < 3) {
            value = '0' + value; // Adiciona zeros à esquerda até ter pelo menos 3 dígitos
        }

        let formattedValue = value.slice(0, -2) + '.' + value.slice(-2); // Insere o ponto antes dos últimos 2 dígitos
        input.value = formattedValue.replace(/^0+(?=\d)/, ''); // Remove zeros desnecessários no início
    }

    document.querySelectorAll('.rtl-number-input').forEach(input => {
        input.addEventListener('input', function() {
            formatNumberInput(this);
        });

        input.addEventListener('blur', function() {
            if (this.value === '') {
                return;
            }
            formatNumberInput(this, true);
        });

        // Não formata o valor inicial ao carregar a página
    });
});