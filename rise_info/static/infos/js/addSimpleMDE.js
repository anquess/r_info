var simplemde;
function makeSimplemde(check) {
    if(check){
        return new SimpleMDE({
            element: document.getElementById("id_content"),
            toolbar: ["heading-1", "heading-2", "bold", "italic", "strikethrough", "|",
            "horizontal-rule", "unordered-list", "ordered-list", "code", "table", "image", "|",
            "preview", "fullscreen", "side-by-side", {
                name : "guid",
                className : "fa fa-question-circle",
                action : function (){window.open("https://simplemde.com/markdown-guide", "_blank");},
                title : "help"
            }]
        });
    }else{
        simplemde.toTextArea();
        return null;
    }
}
simplemde = makeSimplemde(document.getElementById("id_is_rich_text").checked);
