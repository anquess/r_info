function clickCheck(checked_id, text_id, is_text_clear) {
    if (document.getElementById(checked_id).checked === true) {
        document.getElementById(text_id).type = 'text';
    } else {
        if (is_text_clear) {
            document.getElementById(text_id).value = '';
            if (text_id === 'offices-input') {
                var office_display = document.getElementById('offices-display');
                var office_values = document.getElementById('offices-values');
                while (office_display.firstChild) {
                    office_display.removeChild(office_display.firstChild);
                }
                while (office_values.firstChild) {
                    office_values.removeChild(office_values.firstChild);
                }

            } else if (text_id === 'eqtypes-input') {
                var eqtype_display = document.getElementById('eqtypes-display');
                var eqtype_values = document.getElementById('eqtypes-values');
                while (eqtype_display.firstChild) {
                    eqtype_display.removeChild(eqtype_display.firstChild);
                }
                while (eqtype_values.firstChild) {
                    eqtype_values.removeChild(eqtype_values.firstChild);
                }

            }
        }
        document.getElementById(text_id).type = 'hidden';
    }
}