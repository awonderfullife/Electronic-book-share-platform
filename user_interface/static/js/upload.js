$('#upload-form').on('submit',(function(e) {
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        type: 'POST',
        url: "/api/v1/upload",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log("success");
            console.log(data);
            $("#upload").modal("hide");
            $('#upload-success').click();
        },
        error: function(data) {
            console.log("error");
            console.log(data);
        }
    });
}));
