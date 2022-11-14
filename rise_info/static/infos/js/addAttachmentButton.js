$(function () {
    var totalManageElement = $('input#id_attachmentfile_set-TOTAL_FORMS');
    var currentFileCount = parseInt(totalManageElement.val());
    $('button#add').on('click', function () {
        var rowElement = $('<div>', {
            class: 'row pb-2',
        });
        var col5_1Element = $('<div>', {
            class: 'col-5',
        });
        var col2Element = $('<div>', {
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

$(function () {
    var totalManageElement = $('input#id_circumstances_set-TOTAL_FORMS');
    var currentEventCount = parseInt(totalManageElement.val());
    $('button#add_event').on('click', function () {
        var currentEventDate = $('input#id_circumstances_set-' + (currentEventCount - 1) + '-date').val();
        var currentEventTime = $('input#id_circumstances_set-' + (currentEventCount - 1) + '-time').val();
        var rowElement = $('<div>', {
            class: 'row',
        });
        var col2_date_Element = $('<div>', {
            class: 'col-2',
        });
        var col2_time_Element = $('<div>', {
            class: 'col-2',
        });
        var col7_Element = $('<div>', {
            class: 'col-7',
        });
        var col1_Element = $('<div>', {
            class: 'col-1',
        });
        var dateElement = $('<input>', {
            class: 'form-control',
            type: 'date',
            name: 'circumstances_set-' + currentEventCount + '-date',
            id: 'id_circumstances_set-' + currentEventCount + '-date',
            value: currentEventDate,
        });
        var timeElement = $('<input>', {
            class: 'form-control',
            type: 'time',
            name: 'circumstances_set-' + currentEventCount + '-time',
            id: 'id_circumstances_set-' + currentEventCount + '-time',
            value: currentEventTime,
        });
        var eventElement = $('<textarea>', {
            class: 'form-control',
            type: 'text',
            name: 'circumstances_set-' + currentEventCount + '-event',
            id: 'id_circumstances_set-' + currentEventCount + '-event',
            cols: '40',
            rows: '2',
        });
        var delElement = $('<input>', {
            class: 'form-check-input',
            type: 'checkbox',
            name: 'circumstances_set-' + currentEventCount + '-DELETE',
            id: 'id_circumstances_set-' + currentEventCount + '-DELETE',
        });
        col2_date_Element.append(dateElement);
        col2_time_Element.append(timeElement);
        col7_Element.append(eventElement);
        col1_Element.append(delElement);
        rowElement.append(col2_date_Element);
        rowElement.append(col2_time_Element);
        rowElement.append(col7_Element);
        rowElement.append(col1_Element);
        $('div#event-area').append(rowElement);
        currentEventCount += 1;
        totalManageElement.attr('value', currentEventCount);

    });
});


function setUpElement(id) {
    var elment = document.getElementById(id);
    elment.disabled = false;
    elment.hidden = false;
    return elment;
}
function tearDownElement(elment) {
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
