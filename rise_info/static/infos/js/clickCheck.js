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

            }
        }
        document.getElementById(text_id).type = 'hidden';
    }
}