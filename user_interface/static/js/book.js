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
            $('#book-img').attr('src', data.img_url);
            $('#name').html(data.name);
            $('#uploader').html(data.uploader);
            $('#upload-time').html(data.created_at);
            $('#download-time').html(data.download_time);
            $('#score').html(data.score);
            $('#intro p').html(data.description);
        },
    });
}

getBook();
