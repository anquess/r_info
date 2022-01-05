function clickCheck(checked_id, text_id){
    if(document.getElementById(checked_id).checked === true){
        document.getElementById(text_id).type = 'text';
    }else{
        document.getElementById(text_id).value = '';
        document.getElementById(text_id).type ='hidden';
    }
}