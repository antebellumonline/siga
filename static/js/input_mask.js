/* static/js/input_mask.js */
document.addEventListener("DOMContentLoaded", function () {
    function applyInputMasks() {
        const timeInputs = document.querySelectorAll("[data-mask='time']");
        
        timeInputs.forEach(input => {
            input.addEventListener("input", function (event) {
                let value = event.target.value.replace(/\D/g, ""); // Remove caracteres não numéricos
                
                if (value.length > 6) value = value.slice(0, 6); // Limita a 6 dígitos
                
                let formattedValue = "";
                if (value.length > 4) {
                    formattedValue = `${value.slice(0, 2)}:${value.slice(2, 4)}:${value.slice(4, 6)}`;
                } else if (value.length > 2) {
                    formattedValue = `${value.slice(0, 2)}:${value.slice(2, 4)}`;
                } else {
                    formattedValue = value;
                }

                event.target.value = formattedValue;
            });

            input.addEventListener("blur", function (event) {
                let value = event.target.value;
                if (value.length === 5) event.target.value += ":00"; // Adiciona segundos padrão
            });
        });
    }

    applyInputMasks();
});
