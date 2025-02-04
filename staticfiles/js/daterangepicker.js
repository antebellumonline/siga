/* static/js/daterangepicker.js */
document.addEventListener("DOMContentLoaded", function() {
    $('.daterange').daterangepicker({
        startDate: moment(),
        endDate: moment(),
        locale: {
            format: 'DD/MM/YYYY',
            applyLabel: 'Aplicar',
            cancelLabel: 'Cancelar',
            fromLabel: 'De',
            toLabel: 'Até',
            weekLabel: 'S',
            customRangeLabel: 'Personalizado',
            monthNames: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
            daysOfWeek: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
            firstDay: 1
        },
        opens: 'left'
    }, function(start, end) {
        $('.daterange').val(start.format('DD/MM/YYYY') + ' - ' + end.format('DD/MM/YYYY'));
    });

    $('.daterange').on('cancel.daterangepicker', function() {
        $(this).val('');
    });
});