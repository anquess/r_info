function clickCheck(checked_id, text_id, is_text_clear) {
    if (document.getElementById(checked_id).checked === true) {
        document.getElementById(text_id).type = 'text';
    } else {
        if (is_text_clear) {
            document.getElementById(text_id).value = '';
        }
        document.getElementById(text_id).type = 'hidden';
    }
}