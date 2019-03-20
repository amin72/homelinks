$(document).ready(function() {
    // on keyup event preview value of title link
    var titleInput = $("#id_title");
    titleInput.on('input', function() {
        $("#preview_title").text(titleInput.val());
    });

    // on keyup event preview value of description link
    var contentInput = $("#id_description");
    contentInput.on('input', function() {
        var markedContent = contentInput.val();
        markedContent = markedContent.replace(/(?:\r\n|\r|\n)/g, '<br>');
        $("#preview_description").html(markedContent);
    });
})
