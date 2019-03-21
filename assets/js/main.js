function set_preview_title(titleInput) {
    $("#preview_title").text(titleInput.val());
}


function set_preview_description(descriptionInput) {
    var descriptionContent = descriptionInput.val();
    descriptionContent = descriptionContent.replace(/(?:\r\n|\r|\n)/g, '<br>');
    $("#preview_description").html(descriptionContent);
}


$(document).ready(function() {
    // on keyup event preview value of title link
    var titleInput = $("#id_title");
    titleInput.on('input', function() {
        set_preview_title(titleInput);
    });

    set_preview_title(titleInput);

    // on keyup event preview value of description link
    var descriptionInput = $("#id_description");
    descriptionInput.on('input', function() {
        set_preview_description(descriptionInput);
    });

    set_preview_description(descriptionInput);
})
