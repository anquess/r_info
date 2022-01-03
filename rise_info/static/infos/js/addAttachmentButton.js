$(function(){
    var totalManageElement = $('input#id_attachmentfile_set-TOTAL_FORMS');
    var currentFileCount = parseInt(totalManageElement.val());
    $('button#add').on('click', function(){
        var rowElement = $('<div>', {
            class: 'row pb-2',
        });
        var col5_1Element =$('<div>', {
            class: 'col-5',
        }); 
        var col5_2Element =$('<div>', {
            class: 'col-5',
        }); 
        var col2Element =$('<div>', {
            class: 'col-2',
        });
        var fileElement = $('<input>', {
            class: 'form-control',
            type: 'file',
            name: 'attachmentfile_set-' + currentFileCount + '-file',
            id: 'id_attachmentfile_set-' + currentFileCount + '-file',
        });
        var delElement = $('<input>', {
            class: 'form-check-input',
            type: 'checkbox',
            name: 'attachmentfile_set-' + currentFileCount + '-DELETE',
            id: 'id_attachmentfile_set-' + currentFileCount + '-DELETE',
        });
        var delLabelElement = $('<label>', {
            class: 'form-check-label',
            for: 'id_attachmentfile_set-' + currentFileCount + '-DELETE',
        });
        delLabelElement.text("削除")
        col5_1Element.append(fileElement);
        col2Element.append(delElement);
        col2Element.append(delLabelElement);
        rowElement.append(col5_1Element);
        rowElement.append(col2Element);
        $('div#file-area').append(rowElement);
        currentFileCount += 1;
        totalManageElement.attr('value', currentFileCount);
    });
});

function setUpElement(id){
	var elment = document.getElementById(id);
	elment.disabled = false;
	elment.hidden = false;
	return elment;
}
function tearDownElement(elment){
	elment.disabled = true;
	elment.hidden = true;
}
function copy(id) {
	var copyText = setUpElement(id);
	copyText.select();
	document.execCommand("copy");
	tearDownElement(copyText);
}
function change(id) {
	var buttton = setUpElement(id);
	buttton.disabled = true;
	buttton.hidden = true;
}
