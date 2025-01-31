/* static/js/select2.js */
document.addEventListener("DOMContentLoaded", function() {
    $.getScript("/static/select2/js/select2.min.js", function() {
        $('.select2').select2({
            placeholder: 'Selecione uma Opção',
            allowClear: true
        });
    });
});