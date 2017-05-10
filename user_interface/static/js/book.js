function getBook() {
    var id = + window.location.pathname.split('/')[2];
    $.ajax({
        type: 'GET',
        url: '/api/v1/ebook',
        data: {
            'id': id,
        },
        success: function(data) {
            console.log(data);
            book = data;
            $('#book-img').attr('src', data.img_url);
            $('#name').html(data.name);
            $('#uploader').html(data.uploader);
            $('#upload-time').html(data.created_at);
            $('#download-times').html(data.download_times);
            $('#score').html(data.score);
            $('#need_score').html(data.score);
            $('#confirm-score').html(data.score);
            $('#intro p').html(data.description);
        },
    });
}

function download_verify() {
    var id = + window.location.pathname.split('/')[2];
    $.ajax({
        type: 'GET',
        url: '/api/v1/download_verify',
        data: {
            'id': id,
        },
        success: function(data) {
            console.log(data);
            $('#book-img').attr('src', data.img_url);
            $('#name').html(data.name);
            $('#uploader').html(data.uploader);
            $('#upload-time').html(data.created_at);
            $('#download-times').html(data.download_times);
            $('#score').html(data.score);
            $('#intro p').html(data.description);
            $('#confirm').modal('show');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            if (jqXHR.status == 400) {
                $('#not-login').modal('show');
            } else if (jqXHR.status == 500) {
                $('#need-more-score').modal('show');
                $('#curr_score').html(jqXHR.responseJSON.current_score);
            }
        },
    });
}

getBook();
$('#buy').on('click', download_verify);
