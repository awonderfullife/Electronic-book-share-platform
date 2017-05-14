$('#upload-form').on('submit',(function(e) {
    e.preventDefault();
    var formData = new FormData(this);
    var progressBar = $("#progress-bar");
    $.ajax({
        xhr: function() {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                console.log(evt);
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    percentComplete = parseInt(percentComplete * 100);
                    progressBar.css('width', percentComplete + '%');
                    progressBar.html(percentComplete + '%');
                    console.log(percentComplete);
                    if (percentComplete === 100) {
                        progressBar.html("Success!");
                    }
                }
            }, false);
            return xhr;
        },
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
