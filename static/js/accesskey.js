/* static/js/accesskey.js */
document.addEventListener('DOMContentLoaded', function() {
    // Definindo os accesskeys para cada botão
    const accessKeys = {
        'btn-home': 'i',
        'btn-new': 'n',
        'btn-list': 'b',
        'btn-save': 's',
        'btn-edit': 'e',
        'btn-delete': 'x',
        'btn-return': 'r',
        'btn-clear': 'l',
        'btn-excel': 'e',
        'btn-pdf': 'p'
    };

    // Iterando sobre cada botão e definindo o accesskey
    for (const [className, key] of Object.entries(accessKeys)) {
        const button = document.querySelector(`.${className}`);
        if (button) {
            button.setAttribute('accesskey', key);
        }
    }
});
