function setMaxlength(id){
    $(id).maxlength({
        alwaysShow: true,
        warningClass: "label label-success",
        limitReachedClass: "label label-danger"
    });
}